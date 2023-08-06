from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ModelConfig(BaseModel):
    name: str = Field(
        description='The name of the backbone model that will be fine-tuned.'
    )
    freeze: bool = Field(
        default=False,
        description=(
            'If set to True all layers in the backbone model except the last '
            'one will be freezed.'
        ),
    )
    output_dim: Optional[int] = Field(
        default=None,
        description=(
            'The embedding model\'s output dimensionality. If set, a projection '
            'head will be attached to the backbone model.'
        ),
    )
    options: Dict[str, Any] = Field(
        default_factory=lambda: {},
        description=(
            'Additional arguments to pass to the backbone model construction. These '
            'are model specific options and are different depending on the model you '
            'choose.'
        ),
    )


class DataConfig(BaseModel):
    train_data: str = Field(
        description='The training data to use for fine-tuning the model.'
    )
    eval_data: Optional[str] = Field(
        default=None,
        description=(
            'Optional evaluation data to use for the fine-tuning run. '
            'Validation loss is computed per epoch agaist this dataset.'
        ),
    )
    num_workers: int = Field(
        default=8, description='Number of workers used by the dataloaders.'
    )


class CallbackConfig(BaseModel):
    name: str = Field(description='The name of the callback.')
    options: Dict[str, Any] = Field(
        default_factory=lambda: {},
        description='Arguments to pass to the callback construction.',
    )


class HyperParametersConfig(BaseModel):
    loss: str = Field(
        default='TripletMarginLoss',
        description=(
            'Name of the loss function to use for fine-tuning. See '
            'https://kevinmusgrave.github.io/pytorch-metric-learning/losses/ for '
            'available options.'
        ),
    )
    optimizer: str = Field(
        default='Adam',
        description=(
            'Name of the optimizer that will be used for fine-tuning. See '
            'https://pytorch.org/docs/stable/optim.html for available options.'
        ),
    )
    optimizer_options: Dict[str, Any] = Field(
        default_factory=lambda: {},
        description='Specify arguments to pass to the optimizer construction.',
    )
    miner: Optional[str] = Field(
        default=None,
        description=(
            'Specify the miner that will be used for fine-tuning. See '
            'https://kevinmusgrave.github.io/pytorch-metric-learning/miners/ for '
            'available options.'
        ),
    )
    miner_options: Dict[str, Any] = Field(
        default_factory=lambda: {},
        description=(
            'Specify arguments to pass to the miner construction. See '
            'https://kevinmusgrave.github.io/pytorch-metric-learning/miners/ for '
            'detailed information about all possible attributes.'
        ),
    )
    batch_size: int = Field(default=128, description='The training batch size.')
    learning_rate: Optional[float] = Field(
        default=None,
        description=(
            'The learning rate to use during training. If given, this argument '
            'overwrites the optimizer default learning rate or the learning rate '
            'specified in the optimizer options.'
        ),
    )
    epochs: int = Field(default=10, description='Number of fine-tuning epochs')
    scheduler_step: str = Field(
        default='batch',
        description=(
            'At which interval should the learning rate scheduler\'s '
            'step function be called. Valid options are `batch` and `epoch`.'
        ),
    )


class RunConfig(BaseModel):
    model: ModelConfig = Field(description='Model configuration.')
    data: DataConfig = Field(description='Data configuration.')
    callbacks: List[CallbackConfig] = Field(
        default_factory=lambda: [],
        description='List of callbacks that will be used during fine-tuning.',
    )
    hyper_parameters: HyperParametersConfig = Field(
        default=HyperParametersConfig(), description='Hyper-parameter configuration.'
    )
    run_name: Optional[str] = Field(default=None, description='Specify a run name.')
    experiment_name: Optional[str] = Field(
        default=None, description='Specify an experiment name.'
    )
