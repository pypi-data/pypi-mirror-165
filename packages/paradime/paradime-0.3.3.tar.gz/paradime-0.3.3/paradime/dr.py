"""Main module of paraDime.

The :mod:`paradime.dr` module implements the main functionality of paraDime.
This includes the :class:`paradime.dr.ParametricDR` class, as well as
:class:`paradime.dr.Dataset` and :class:`paradime.dr.TrainingPhase`.
"""

import copy
from typing import Union, Literal, Optional

import numpy as np
import torch

from paradime import exceptions
from paradime import models
from paradime import relationdata
from paradime import relations
from paradime import loss as pdloss
from paradime.types import Data, TensorLike
from paradime import utils


class Dataset(torch.utils.data.Dataset, utils._ReprMixin):
    """A dataset for dimensionality reduction.

    Constructs a PyTorch :class:torch.utils.data.Dataset from the given data
    in such a way that each item or batch of items is a dictionary with
    PyTorch tensors as values. If only a single numpy array or PyTorch tensor
    is passed, this data will be available under the ``'data'`` key of the
    dict. Alternatively, a dict of tensors and/or arrays can be passed, which
    allows additional data such as labels for supervised learning. By default,
    an entry for indices is added to the dict, if it is not yet included in the
    passed dict.

    Args:
        data: The data, passed either as a single numpy array or PyTorch
            tensor, or as a dictionary containing multiple arrays and/or
            tensors.
    """

    def __init__(self, data: Data):

        self.data: dict[str, torch.Tensor] = {}

        if isinstance(data, (np.ndarray, torch.Tensor)):
            data = {"data": data}
        elif not isinstance(data, dict):
            raise ValueError(
                "Expected numpy array, PyTorch tensor, or dict "
                f"instead of {type(data)}."
            )
        else:
            if "data" not in data:
                raise AttributeError(
                    "Dataset expects a dict with a 'data' entry."
                )
        for k in data:
            val = data[k]
            if not isinstance(val, (np.ndarray, torch.Tensor)):
                raise ValueError(
                    f"Value for key {k} is not a numpy array "
                    "or PyTorch tensor."
                )
            if len(val) != len(data["data"]):
                raise ValueError(
                    "Dataset dict must have values of equal length."
                )
            self.data[k] = utils.convert.to_torch(data[k])

        if "indices" not in self.data:
            self.data["indices"] = torch.arange(len(self))

    def __len__(self) -> int:
        return len(self.data["data"])

    def __getitem__(self, index) -> dict[str, torch.Tensor]:
        out = {}
        for k in self.data:
            out[k] = self.data[k][index]
        return out


class NegSampledEdgeDataset(torch.utils.data.Dataset):
    """A dataset that supports negative edge sampling.

    Constructs a PyTorch :class:`torch.utils.data.Dataset` suitable for
    negative sampling from a regular :class:Dataset. The passed relation
    data, along with the negative samplnig rate ``r``, is used to inform the
    negative sampling process. Each \"item\" ``i`` of the resulting dataset
    is essentially a small batch of items, including the item ``i`` of the
    original dataset, one of it's actual neighbors, and ``r`` random other
    items that are considered to not be neighbors of ``i``. Remaining data
    from the original dataset is collated using PyTorch's
    :func:`torch.utils.data.default_collate` method.

    Args:
        data: The data in the form of a ParaDime :class:`paradime.dr.Dataset`.
        relations: A :class:`paradime.relationdata.RelationData` object with
            the edge data used for negative edge sampling.
        neg_sampling_rate: The negative sampling rate.
    """

    def __init__(
        self,
        dataset: Dataset,
        relations: relationdata.RelationData,
        neg_sampling_rate: int = 5,
    ):

        self.dataset = dataset
        self.p_ij = relations.to_sparse_array().data.tocoo()
        self.weights = self.p_ij.data
        self.neg_sampling_rate = neg_sampling_rate

    def __len__(self) -> int:
        return len(self.dataset)

    def __getitem__(self, idx: int) -> dict[str, torch.Tensor]:
        # the following assumes that the input relations are symmetric.
        # if they are not, the rows and cols should be shuffled

        # make nsr + 1 copies of row index
        rows = torch.full(
            (self.neg_sampling_rate + 1,), self.p_ij.row[idx], dtype=torch.long
        )

        # pick nsr + 1 random col indices (negative samples)
        cols = torch.randint(
            self.p_ij.shape[0], (self.neg_sampling_rate + 1,), dtype=torch.long
        )
        # set only one to an actual neighbor
        cols[0] = self.p_ij.col[idx]

        # make simplified p_ij (0 or 1)
        p_simpl = torch.zeros(self.neg_sampling_rate + 1, dtype=torch.float32)
        p_simpl[0] = 1

        indices = torch.tensor(
            np.unique(np.concatenate((rows.numpy(), cols.numpy())))
        )

        edge_data = {"row": rows, "col": cols, "rel": p_simpl}

        edge_data["from_to_data"] = torch.stack(
            (self.dataset.data["data"][rows], self.dataset.data["data"][cols])
        )

        remaining_data = torch.utils.data.default_collate(
            [self.dataset[i] for i in indices]
        )

        return {**remaining_data, **edge_data}


def _collate_edge_batch(
    raw_batch: list[dict[str, torch.Tensor]]
) -> dict[str, torch.Tensor]:

    indices, unique_ids = np.unique(
        torch.concat([i["indices"] for i in raw_batch]), return_index=True
    )

    collated_batch = {"indices": torch.tensor(indices)}

    for k in raw_batch[0]:
        if k in ["row", "col", "rel"]:
            collated_batch[k] = torch.concat([i[k] for i in raw_batch])
        elif k == "from_to_data":
            collated_batch[k] = torch.concat([i[k] for i in raw_batch], dim=1)
        else:
            collated_batch[k] = torch.concat([i[k] for i in raw_batch])[
                torch.tensor(unique_ids)
            ]

    return collated_batch


class TrainingPhase(utils._ReprMixin):
    """A collection of parameter settings for a single phase in the
    training of a :class:`paradime.dr.ParametricDR` instance.

    Args:
        name: The name of the training phase.
        epochs: The number of epochs to run in this phase. In standard
            item-based sampling, the model sees every item once per epoch
            In the case of negative edge sampling, this is not guaranteed, and
            an epoch instead comprises ``batches_per_epoch`` batches (see
            parameter description below).
        batch_size: The number of items/edges in a batch. In standard
            item-based sampling, a batch has this many items, and the edges
            used for batch relations are constructed from the items. In the
            case of negative edge sampling, this is the number of sampled
            *positive* edges. The total number of edges is higher by a factor
            of ``r + 1``, where ``r`` is the negative sampling rate. The same holds
            for the number of items (apart from possible duplicates, which can
            result from the edge sampling and are removed).
        batches_per_epoch: The number of batches per epoch. This parameter
            only has an effect for negative edge sampling, where the number
            of batches per epoch is not determined by the dataset size and the
            batch size. If this parameter is set to -1 (default), an epoch
            will comprise a number of batches that leads to a total number of
            sampled *items* roughly equal to the number of items in the
            dataset. If this parameter is set to an integer, an epoch will
            instead comprise that many batches.
        sampling: The sampling strategy, which can be either ``'standard'``
            (simple item-based sampling; default) or ``'negative_edge'``
            (negative edge sampling).
        edge_rel_key: The key under which to find the global relations that
            should be used for negative edge sampling.
        neg_sampling_rate: The number of negative (i.e., non-neighbor) edges
            to sample for each real neighborhood edge.
        loss: The loss that is minimized in this training phase.
        optimizer: The optmizer to use for loss minimization.
        learning_rate: The learning rate used in the optimization.
        report_interval: How often the loss should be reported during
            training, given in terms of epochs. E.g., with a setting of 5,
            the loss will be reported every 5 epochs.
        kwargs: Additional kwargs that are passed on to the optimizer.
    """

    def __init__(
        self,
        name: Optional[str] = None,
        epochs: int = 5,
        batch_size: int = 50,
        batches_per_epoch: int = -1,
        sampling: Literal["standard", "negative_edge"] = "standard",
        edge_rel_key: str = "rel",
        neg_sampling_rate: int = 5,
        loss: pdloss.Loss = pdloss.Loss(),
        optimizer: type = torch.optim.Adam,
        learning_rate: float = 0.01,
        report_interval: int = 5,
        **kwargs,
    ):

        self.name = name
        self.epochs = epochs
        self.batch_size = batch_size
        self.batches_per_epoch = batches_per_epoch
        self.sampling = sampling
        if self.sampling not in ["standard", "negative_edge"]:
            raise ValueError(f"Unknown sampling option {self.sampling}.")
        self.edge_rel_key = edge_rel_key
        self.neg_sampling_rate = neg_sampling_rate

        self.loss = loss

        self.optimizer = optimizer
        self.learning_rate = learning_rate
        self.report_interval = report_interval
        self.kwargs = kwargs

        if not issubclass(self.optimizer, torch.optim.Optimizer):
            raise ValueError(
                f"{self.optimizer} is not a valid PyTorch optimizer."
            )


RelOrRelDict = Union[relations.Relations, dict[str, relations.Relations]]


class ParametricDR(utils._ReprMixin):
    """A general parametric dimensionality reduction routine.

    Args:
        model: The PyTorch :class:`torch.nn.module` whose parameters are
            optimized during training.
        in_dim: The numer of dimensions of the input data, used to construct a
            default model in case none is specified. If a dataset is specified
            at instantiation, the correct value for this parameter will be
            inferred from the data dimensions.
        out_dim: The number of output dimensions (i.e., the dimensionality of
            the embedding).
        hidden_dims: Dimensions of hidden layers for the default fully
            connected model that is created if no model is specified.
        dataset: The dataset on which to perform the training, passed either
            as a single numpy array or PyTorch tensor, a dictionary containing
            multiple arrays and/or tensors, or a :class:`paradime.dr.Dataset`
            Datasets can be registerd after instantiation using the
            :meth:`register_dataset` class method.
        global_relations: A single :class:`paradime.relations.Relations`
            instance or a dictionary with multiple
            :class:`paradime.relations.Relations` instances. Global relations
            are calculated once for the whole dataset before training.
        batch_relations: A single :class:`paradime.relations.Relations`
            instance or a dictionary with multiple
            :class:`paradime.relations.Relations` instances. Batch relations
            are calculated during training for each batch and are compared to
            an appropriate subset of the global relations by a
            :class:`paradime.loss.RelationLoss`.
        training_defaults: A :class:`paradime.dr.TrainingPhase` object with
            settings that override the default values of all other training
            phases. This parameter is useful to avoid having to repeatedly
            set parameters to the same non-default value across training
            phases. Defaults can also be specified after isntantiation using
            the :meth:`set_training_deafults` class method.
        training_phases: A single :class:`paradime.dr.TrainingPhase` object or
            a list of :class:`paradime.dr.TrainingPhase` objects defining the
            training phases to be run. Training phases can also be added
            after instantiation using the :meth:`add_training_pahse` class
            method.
        use_cuda: Whether or not to use the GPU for training.
        verbose: Verbosity flag. This setting overrides all verbosity settings
            of relations, transforms and/or losses used within the parametric
            dimensionality reduction.

    Attributes:
        device: The device on which the model is allocated (depends on the
            value specified for ``use_cuda``).
    """

    def __init__(
        self,
        model: Optional[torch.nn.Module] = None,
        in_dim: Optional[int] = None,
        out_dim: int = 2,
        hidden_dims: list[int] = [100, 50],
        dataset: Optional[Union[Data, Dataset]] = None,
        global_relations: Optional[RelOrRelDict] = None,
        batch_relations: Optional[RelOrRelDict] = None,
        training_defaults: TrainingPhase = TrainingPhase(),
        training_phases: Optional[list[TrainingPhase]] = None,
        use_cuda: bool = False,
        verbose: bool = False,
    ):

        self.verbose = verbose

        self._dataset: Optional[Dataset] = None
        self._dataset_registered = False
        if dataset is not None:
            self.register_dataset(dataset)

        self.model: torch.nn.Module

        if model is None:
            if in_dim is None and not self._dataset_registered:
                raise ValueError(
                    "A value for 'in_dim' must be given if no model or "
                    "dataset is specified."
                )
            elif in_dim is None and isinstance(self.dataset, Dataset):
                try:
                    in_dim = self.dataset.data["data"].shape[-1]
                except KeyError:
                    pass
            if isinstance(in_dim, int):
                self.model = models.FullyConnectedEmbeddingModel(
                    in_dim,
                    out_dim,
                    hidden_dims,
                )
            else:
                raise KeyError(
                    "Failed to infer data dimensionality from dataset."
                )
        else:
            self.model = model

        if isinstance(global_relations, relations.Relations):
            self.global_relations = {"rel": global_relations}
        elif global_relations is not None:
            self.global_relations = global_relations
        else:
            self.global_relations = {}
        for k in self.global_relations:
            self.global_relations[k]._set_verbosity(self.verbose)

        self.global_relation_data: dict[str, relationdata.RelationData] = {}
        self._global_relations_computed = False

        if isinstance(batch_relations, relations.Relations):
            self.batch_relations = {"rel": batch_relations}
        elif batch_relations is not None:
            self.batch_relations = batch_relations
        else:
            self.batch_relations = {}
        for k in self.batch_relations:
            self.batch_relations[k]._set_verbosity(self.verbose)

        self.training_defaults = training_defaults

        self.training_phases: list[TrainingPhase] = []
        if training_phases is not None:
            for tp in training_phases:
                self.add_training_phase(training_phase=tp)

        self.use_cuda = use_cuda
        if use_cuda:
            self.model.cuda()

        self.trained = False

    @property
    def dataset(self) -> Dataset:
        if isinstance(self._dataset, Dataset):
            return self._dataset
        else:
            raise exceptions.NoDatasetRegisteredError(
                "Attempted to access a dataset, but none was registered."
            )

    @property
    def device(self) -> torch.device:
        device = torch.device("cpu")
        for p in self.model.parameters():
            device = p.device
            break
        return device

    def __call__(self, X: TensorLike) -> torch.Tensor:

        return self.embed(X)

    def _call_model_method_by_name(
        self,
        method_name: str,
        X: TensorLike,
    ) -> torch.Tensor:

        X = utils.convert.to_torch(X)

        if self.use_cuda:
            X = X.cuda()

        if not hasattr(self.model, method_name):
            raise AttributeError(f"Model has no {method_name} method.")
        elif not callable(getattr(self.model, method_name)):
            raise ValueError(
                f"Attribute {method_name} of model is not a callable."
            )

        if self.trained:
            return getattr(self.model, method_name)(X)
        else:
            raise exceptions.NotTrainedError(
                "DR instance is not trained yet. Call 'train' with "
                "appropriate arguments before calling the model."
            )

    @torch.no_grad()
    def apply(
        self, X: TensorLike, method: Optional[str] = None
    ) -> torch.Tensor:
        """Applies the model to input data.

        Applies the model to an input tensor after first switching off
        PyTorch's automatic gradient tracking. This method also ensures that
        the resulting output tensor is on the CPU. The ``method`` parameter
        allows calling of any of the model's methods in this way, but by
        default, the model's ``__call__`` method will be used (which wraps
        around ``forward``.)

        Args:
            X: A numpy array or PyTorch tensor with the input data.
            method: The name of the model method to be applied.
        """

        if method is None:
            method = "__call__"

        return self._call_model_method_by_name(method, X).cpu()

    def embed(self, X: TensorLike) -> torch.Tensor:
        """Embeds data into the learned embedding space using the model's
        ``embed`` method.

        Args:
            X: A numpy array or PyTorch tensor with the data to be embedded.

        Returns:
            A PyTorch tensor with the embedding coordinates for the data.
        """
        return self._call_model_method_by_name("embed", X)

    def classify(self, X: TensorLike) -> torch.Tensor:
        """Classifies data using the model's ``classify`` method.

        Args:
            X: A numpy array or PyTorch tensor with the data to be classified.

        Returns:
            A PyTorch tensor with the predicted class labels for the data.
        """
        return self._call_model_method_by_name("classify", X)

    def set_training_defaults(
        self,
        training_phase: Optional[TrainingPhase] = None,
        epochs: Optional[int] = None,
        batch_size: Optional[int] = None,
        batches_per_epoch: Optional[int] = None,
        sampling: Optional[Literal["standard", "negative_edge"]] = None,
        edge_rel_key: Optional[str] = None,
        neg_sampling_rate: Optional[int] = None,
        loss: Optional[pdloss.Loss] = None,
        optimizer: Optional[type] = None,
        learning_rate: Optional[float] = None,
        report_interval: Optional[int] = 5,
        **kwargs,
    ) -> None:
        """Sets a parametric dimensionality reduction routine's default
        training parameters.

        This methods accepts either a :class:`paradime.dr.TrainingPhase`
        instance or individual parameters passed with the same keyword syntax
        used by :class:`paradime.dr.TrainingPhase`. The specified default
        parameters will be used instead of the regular defaults when adding
        training phases.

        Args:
            training_phase: A :class:`paradime.dr.TrainingPhase` instance with
                the new default settings. Instead of this, individual
                parameters can also be passed. For a full list of training
                phase settings, see :class:`paradime.dr.TrainingPhase`.
        """
        if training_phase is not None:
            self.training_defaults = copy.deepcopy(training_phase)
        if epochs is not None:
            self.training_defaults.epochs = epochs
        if batch_size is not None:
            self.training_defaults.batch_size = batch_size
        if batches_per_epoch is not None:
            self.training_defaults.batch_size = batches_per_epoch
        if sampling is not None:
            self.training_defaults.sampling = sampling
        if edge_rel_key is not None:
            self.training_defaults.edge_rel_key = edge_rel_key
        if neg_sampling_rate is not None:
            self.training_defaults.neg_sampling_rate = neg_sampling_rate
        if loss is not None:
            self.training_defaults.loss = loss
        if optimizer is not None:
            self.training_defaults.optimizer = optimizer
        if learning_rate is not None:
            self.training_defaults.learning_rate = learning_rate
        if report_interval is not None:
            self.training_defaults.report_interval = report_interval
        if kwargs:
            self.training_defaults.kwargs = {
                **self.training_defaults.kwargs,
                **kwargs,
            }

    def add_training_phase(
        self,
        training_phase: Optional[TrainingPhase] = None,
        name: Optional[str] = None,
        epochs: Optional[int] = None,
        batch_size: Optional[int] = None,
        batches_per_epoch: Optional[int] = None,
        sampling: Optional[Literal["standard", "negative_edge"]] = None,
        edge_rel_key: Optional[str] = None,
        neg_sampling_rate: Optional[int] = None,
        loss: Optional[pdloss.Loss] = None,
        optimizer: Optional[type] = None,
        learning_rate: Optional[float] = None,
        report_interval: Optional[int] = None,
        **kwargs,
    ) -> None:
        """Adds a single training phase to a parametric dimensionality
        reduction routine.

        This methods accepts either a :class:`paradime.dr.TrainingPhase`
        instance or individual parameters passed with the same keyword syntax
        used by :class:`paradime.dr.TrainingPhase`.

        Args:
            training_phase: A :class:`paradime.dr.TrainingPhase` instance with
                the new default settings. Instead of this, individual
                parameters can also be passed. For a full list of training
                phase settings, see :class:`paradime.dr.TrainingPhase`.

        Raises:
            :class:`paradime.exceptions.UnsupportedConfigurationError`: This
                error is raised if the type of
                :class:`paradime.relation.Relations` is not compatible with the
                sampling option.
        """
        if training_phase is None:
            training_phase = copy.deepcopy(self.training_defaults)
        assert isinstance(training_phase, TrainingPhase)

        if name is not None:
            training_phase.name = name
        if epochs is not None:
            training_phase.epochs = epochs
        if batch_size is not None:
            training_phase.batch_size = batch_size
        if batches_per_epoch is not None:
            training_phase.batches_per_epoch = batches_per_epoch
        if sampling is not None:
            training_phase.sampling = sampling
        if edge_rel_key is not None:
            training_phase.edge_rel_key = edge_rel_key
        if neg_sampling_rate is not None:
            training_phase.neg_sampling_rate = neg_sampling_rate
        if loss is not None:
            training_phase.loss = loss
        if optimizer is not None:
            training_phase.optimizer = optimizer
        if learning_rate is not None:
            training_phase.learning_rate = learning_rate
        if report_interval is not None:
            training_phase.report_interval = report_interval
        if kwargs:
            training_phase.kwargs = {**training_phase.kwargs, **kwargs}

        if isinstance(
            training_phase.loss, (pdloss.RelationLoss, pdloss.CompoundLoss)
        ):
            training_phase.loss._check_sampling_and_relations(
                training_phase.sampling, self.batch_relations
            )

        self.training_phases.append(training_phase)

    def register_dataset(self, dataset: Union[Data, Dataset]) -> None:
        """Registers a dataset for a parametric dimensionality reduction
        routine.

        Args:
            dataset: The data, passed either as a single numpy array or PyTorch
                tensor, a dictionary containing multiple arrays and/or
                tensors, or a :class:`paradime.dr.Dataset`.
        """
        if self.verbose:
            utils.logging.log("Registering dataset.")
        if isinstance(dataset, Dataset):
            self._dataset = dataset
        else:
            self._dataset = Dataset(dataset)

        self._dataset_registered = True

    def add_to_dataset(self, data: dict[str, TensorLike]) -> None:
        """Adds additional data entries to an existing dataset.

        Useful for injecting additional data entries that can be derived from
        other data, so that they don't have to be added manually (e.g., PCA
        for pretraining routines).

        Args:
            data: A dict containing the data tensors to be added to the
                dataset.
        """
        if not self._dataset_registered:
            raise exceptions.NoDatasetRegisteredError(
                "Cannot inject additional data before registering a dataset."
            )
        for k in data:
            if self.verbose:
                if hasattr(self.dataset, k):
                    utils.logging.log(f"Overwriting entry '{k}' in dataset.")
                else:
                    utils.logging.log(f"Adding entry '{k}' to dataset.")
            self.dataset.data[k] = utils.convert.to_torch(data[k])

    def compute_global_relations(self, force: bool = False) -> None:
        """Computes the global relations.

        The computed relation data are stored in the instance's
        ``global_relation_data`` attribute.

        Args:
            force: Whether or not to force a new computation, when relations
                have been previously computed for the same instance.
        """

        if not self._dataset_registered:
            raise exceptions.NoDatasetRegisteredError(
                "Cannot compute global relations before registering dataset."
            )
        assert isinstance(self.dataset, Dataset)

        if force or not self._global_relations_computed:

            for k in self.global_relations:
                if self.verbose:
                    utils.logging.log(f"Computing global relations '{k}'.")
                rel = self.global_relations[k]
                self.global_relation_data[k] = rel.compute_relations(
                    self.dataset.data[rel.data_key]
                )

        self._global_relations_computed = True

    def _prepare_loader(
        self, training_phase: TrainingPhase
    ) -> torch.utils.data.DataLoader:

        if not self._dataset_registered:
            raise exceptions.NoDatasetRegisteredError(
                "Cannot prepare loader before registering dataset."
            )
        assert isinstance(self.dataset, Dataset)

        if not self._global_relations_computed:
            raise exceptions.RelationsNotComputedError(
                "Cannot prepare loader before computing global relations."
            )

        if training_phase.sampling == "negative_edge":
            if training_phase.edge_rel_key not in self.global_relation_data:
                raise KeyError(
                    f"Global relations '{training_phase.edge_rel_key}' "
                    "not specified."
                )
            if training_phase.batches_per_epoch == -1:
                num_edges = max(
                    training_phase.batch_size,
                    int(
                        np.ceil(
                            len(self.dataset)
                            / (training_phase.neg_sampling_rate + 1)
                        )
                    ),
                )
            else:
                num_edges = (
                    training_phase.batch_size * training_phase.batches_per_epoch
                )
            edge_dataset = NegSampledEdgeDataset(
                self.dataset,
                self.global_relation_data[training_phase.edge_rel_key],
                training_phase.neg_sampling_rate,
            )
            sampler = torch.utils.data.WeightedRandomSampler(
                edge_dataset.weights, num_samples=num_edges
            )
            dataloader = torch.utils.data.DataLoader(
                edge_dataset,
                batch_size=training_phase.batch_size,
                collate_fn=_collate_edge_batch,
                sampler=sampler,
            )
        else:
            dataset = self.dataset
            dataloader = torch.utils.data.DataLoader(
                dataset, batch_size=training_phase.batch_size, shuffle=True
            )

        return dataloader

    def _prepare_optimizer(
        self, training_phase: TrainingPhase
    ) -> torch.optim.Optimizer:

        optimizer: torch.optim.Optimizer = training_phase.optimizer(
            self.model.parameters(),
            lr=training_phase.learning_rate,
            **training_phase.kwargs,
        )

        return optimizer

    def _prepare_training(self) -> None:
        """Dummy method to inject code between instantiation and training.

        To be overwritten by subclasses. This allows, e.g., to add default
        training phases outside of a subclass's ``__init__`` but before calling
        the instance's :meth:`train` method.
        """
        pass

    def run_training_phase(self, training_phase: TrainingPhase) -> None:
        """Runs a single training phase.

        Args:
            training_phase: A :class:`paradime.dr.TrainingPhase` instance.
        """
        dataloader = self._prepare_loader(training_phase)
        optimizer = self._prepare_optimizer(training_phase)

        device = self.device

        if self.verbose:
            utils.logging.log(
                f"Beginning training phase '{training_phase.name}'."
            )

        for epoch in range(training_phase.epochs):

            batch: dict[str, torch.Tensor]
            for batch in dataloader:

                optimizer.zero_grad()

                loss = training_phase.loss(
                    self.model,
                    self.global_relation_data,
                    self.batch_relations,
                    batch,
                    device,
                )

                loss.backward()
                optimizer.step()

            training_phase.loss.checkpoint()

            if self.verbose and epoch % training_phase.report_interval == 0:
                # TODO: replace by loss reporting mechanism (GH issue #3)
                utils.logging.log(
                    f"Loss after epoch {epoch}: "
                    f"{training_phase.loss.history[-1]}"
                )

            self.trained = True

    def train(self) -> None:
        """Runs all training phases of a parametric dimensionality reduction
        routine.
        """
        self._prepare_training()
        self.compute_global_relations()

        self.model.train()

        for tp in self.training_phases:
            self.run_training_phase(tp)

        self.model.eval()
