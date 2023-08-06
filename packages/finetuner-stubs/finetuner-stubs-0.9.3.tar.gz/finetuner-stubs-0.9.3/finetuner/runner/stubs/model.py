import abc
from typing import Any, Dict, List, Optional, Tuple, TypeVar, Union

ModelStubType = TypeVar('ModelStubType', bound='_ModelStub')


class _ModelStub(metaclass=abc.ABCMeta):
    name: str
    descriptor: str
    description: str
    task: str
    architecture: str
    builder: str
    embedding_layer: Optional[str]
    input_names: List[str]
    input_shapes: List[Tuple[Union[int, str], ...]]
    input_dtypes: List[str]
    output_name: str
    output_shape: Tuple[Union[int, str], ...]
    dynamic_axes: Dict[str, Dict[int, str]]
    preprocess_types: Dict[str, str]
    collate_types: Dict[str, str]
    preprocess_options: Dict[str, Dict[str, Any]] = {}
    collate_options: Dict[str, Dict[str, Any]] = {}
    options: Dict[str, Any] = {}

    def __init__(
        self,
        preprocess_options: Optional[Dict[str, Dict[str, Any]]] = None,
        collate_options: Optional[Dict[str, Dict[str, Any]]] = None,
        **options: Any
    ) -> None:
        self.options = options
        if preprocess_options:
            self.preprocess_options.update(preprocess_options)
        if collate_options:
            self.collate_options.update(collate_options)

    @property
    @abc.abstractmethod
    def name(self) -> str:
        ...


class _CNNStub(_ModelStub, metaclass=abc.ABCMeta):
    """CNN model stub."""

    task = 'image-to-image'
    architecture = 'cnn'
    builder = 'CNNBuilder'
    input_names = ['image']
    input_dtypes = ['float32']
    output_name = 'embedding'
    dynamic_axes = {'image': {0: 'batch-size'}, 'embedding': {0: 'batch-size'}}
    preprocess_types = {'image': 'VisionPreprocess'}
    collate_types = {'image': 'DefaultCollate'}
    preprocess_options = {'image': {}}
    collate_options = {'image': {}}

    def __init__(
        self,
        preprocess_options: Optional[Dict[str, Dict[str, Any]]] = None,
        collate_options: Optional[Dict[str, Dict[str, Any]]] = None,
    ):
        super(_CNNStub, self).__init__(
            preprocess_options=preprocess_options, collate_options=collate_options
        )
        self.input_shapes = [
            (
                'batch-size',
                3,
                self.preprocess_options['image'].get('height', 224),
                self.preprocess_options['image'].get('width', 224),
            ),
        ]


class _TextTransformerStub(_ModelStub, metaclass=abc.ABCMeta):
    """Text transformer model stub."""

    task = 'text-to-text'
    architecture = 'transformer'
    builder = 'TextTransformerBuilder'
    input_names = ['input_ids', 'attention_mask']
    input_dtypes = ['int32', 'int32']
    input_shapes = [
        ('batch-size', 'sequence-length'),
        ('batch-size', 'sequence-length'),
    ]
    output_name = 'embedding'
    dynamic_axes = {
        'input_ids': {0: 'batch-size', 1: 'sequence-length'},
        'attention_mask': {0: 'batch-size', 1: 'sequence-length'},
        'embedding': {0: 'batch-size'},
    }
    preprocess_types = {'text': 'TextPreprocess'}
    collate_types = {'text': 'TransformersCollate'}
    preprocess_options = {'text': {}}
    collate_options = {'text': {}}

    def __init__(
        self,
        pooling: str = 'mean',
        preprocess_options: Optional[Dict[str, Dict[str, Any]]] = None,
        collate_options: Optional[Dict[str, Dict[str, Any]]] = None,
    ):
        self.collate_options = {
            'text': {'name': self.descriptor, 'truncation': True, 'padding': True}
        }
        super(_TextTransformerStub, self).__init__(
            preprocess_options=preprocess_options,
            collate_options=collate_options,
            pooling=pooling,
        )


class _VisionTransformerStub(_ModelStub, metaclass=abc.ABCMeta):
    """Vision transformer model stub."""

    task = 'image-to-image'
    architecture = 'transformer'
    builder = 'VisionTransformerBuilder'
    input_names = ['pixel_values']
    input_dtypes = ['float32']
    output_name = 'embedding'
    dynamic_axes = {
        'pixel_values': {
            0: 'batch-size',
        },
        'embedding': {0: 'batch-size'},
    }
    preprocess_types = {'image': 'VisionPreprocess'}
    collate_types = {'image': 'VisionTransformersCollate'}
    preprocess_options = {'image': {}}
    collate_options = {'image': {}}

    def __init__(
        self,
        preprocess_options: Optional[Dict[str, Dict[str, Any]]] = None,
        collate_options: Optional[Dict[str, Dict[str, Any]]] = None,
    ):
        self.collate_options = {'image': {'name': self.descriptor}}
        super(_VisionTransformerStub, self).__init__(
            preprocess_options=preprocess_options, collate_options=collate_options
        )
        self.input_shapes = [
            (
                'batch-size',
                3,
                self.preprocess_options['image'].get('height', 224),
                self.preprocess_options['image'].get('width', 224),
            ),
        ]


class MLPStub(_ModelStub):
    """MLP model stub.

    :param input_size: Size of the input representations.
    :param hidden_sizes: A list of sizes of the hidden layers. The last hidden size is
        the output size.
    :param bias: Whether to add bias to each layer.
    :param activation: A string to configure activation function, `relu`, `tanh` or
        `sigmoid`. Set to `None` for no activation.
    :param l2: Apply L2 normalization at the output layer.
    """

    name = 'mlp'
    descriptor = 'mlp'
    description = 'Simple MLP encoder trained from scratch'
    task = 'any'
    architecture = 'mlp'
    builder = 'MLPBuilder'
    embedding_layer = None
    input_names = ['features']
    input_dtypes = ['float32']
    output_name = 'embedding'
    dynamic_axes = {'features': {0: 'batch-size'}, 'embedding': {0: 'batch-size'}}
    preprocess_types = {'features': 'DefaultPreprocess'}
    collate_types = {'features': 'DefaultCollate'}
    preprocess_options = {'features': {}}
    collate_options = {'features': {}}

    def __init__(
        self,
        input_size: int,
        hidden_sizes: Tuple[int] = (),
        bias: bool = True,
        activation: Optional[str] = None,
        l2: bool = False,
        preprocess_options: Optional[Dict[str, Dict[str, Any]]] = None,
        collate_options: Optional[Dict[str, Dict[str, Any]]] = None,
    ):
        super(MLPStub, self).__init__(
            preprocess_options=preprocess_options,
            collate_options=collate_options,
            input_size=input_size,
            hidden_sizes=hidden_sizes,
            bias=bias,
            activation=activation,
            l2=l2,
        )
        self.input_shapes = [('batch-size', input_size)]
        self.output_shape = (
            'batch-size',
            hidden_sizes[-1] if len(hidden_sizes) > 0 else input_size,
        )


class ResNet50Stub(_CNNStub):
    """ResNet50 model stub."""

    name = 'resnet50'
    descriptor = 'resnet50'
    description = 'ResNet50 pre-trained on ImageNet'
    embedding_layer = 'adaptiveavgpool2d_173'
    output_shape = ('batch-size', 2048)


class ResNet152Stub(_CNNStub):
    """ResNet152 model stub."""

    name = 'resnet152'
    descriptor = 'resnet152'
    description = 'ResNet152 pre-trained on ImageNet'
    embedding_layer = 'adaptiveavgpool2d_513'
    output_shape = ('batch-size', 2048)


class EfficientNetB0Stub(_CNNStub):
    """EfficientNetB0 model stub."""

    name = 'efficientnet_b0'
    descriptor = 'efficientnet_b0'
    description = 'EfficientNet B0 pre-trained on ImageNet'
    embedding_layer = 'dropout_254'
    output_shape = ('batch-size', 1280)


class EfficientNetB4Stub(_CNNStub):
    """EfficientNetB4 model stub."""

    name = 'efficientnet_b4'
    descriptor = 'efficientnet_b4'
    description = 'EfficientNet B4 pre-trained on ImageNet'
    embedding_layer = 'dropout_507'
    output_shape = ('batch-size', 1792)


class BERTStub(_TextTransformerStub):
    """BERT model stub."""

    name = 'bert-base-cased'
    descriptor = 'bert-base-cased'
    description = 'BERT model pre-trained on BookCorpus and English Wikipedia'
    embedding_layer = None
    output_shape = ('batch-size', 768)


class SBERTStub(_TextTransformerStub):
    """SentenceTransformer model stub."""

    name = 'sentence-transformers/msmarco-distilbert-base-v3'
    descriptor = 'sentence-transformers/msmarco-distilbert-base-v3'
    description = 'Pretrained BERT, fine-tuned on MS Marco'
    embedding_layer = None
    output_shape = ('batch-size', 768)


class CLIPTextStub(_TextTransformerStub):
    """CLIP text model stub."""

    name = 'clip-text'
    descriptor = 'openai/clip-vit-base-patch32'
    description = 'CLIP pre-trained text transformer encoder'
    builder = 'CLIPTextBuilder'
    embedding_layer = None
    output_shape = ('batch-size', 512)


class CLIPVisionStub(_VisionTransformerStub):
    """CLIP vision model stub."""

    name = 'clip-vision'
    descriptor = 'openai/clip-vit-base-patch32'
    description = 'CLIP pre-trained vision transformer encoder'
    builder = 'CLIPVisionBuilder'
    embedding_layer = None
    output_shape = ('batch-size', 512)
