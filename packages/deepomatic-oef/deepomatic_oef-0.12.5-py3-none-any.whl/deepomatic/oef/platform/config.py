import deepomatic.oef.protos.dataoperation_pb2 as dop

from .helpers.common import is_true
from .helpers.controls import DisplayCondition, ModelControl, SelectControl, SelectOption, InputControl, ToggleControl
from .helpers.section import Section
from .helpers.form import Form
from .helpers.tags import Backend, ViewType


# Define here the models enabled in Vesta
# For CLA and TAG view types
enabled_classification_models = [
    'efficientnet_b0',
    'efficientnet_b1',
    'efficientnet_b2',
    'efficientnet_b3',
    'efficientnet_b4',
    'efficientnet_b5',
    'efficientnet_b6',
    'inception_resnet_v2',
    'inception_v1',
    'inception_v2',
    'inception_v3',
    'inception_v4',
    'resnet_101_v1',
    'resnet_152_v1',
    'resnet_50_v1',
    'mobilenet_v1',
    'mobilenet_v2',
    'vgg_16',
    # VGG 19 is disabled while we solve memory issues with inference
    # 'vgg_19',
]

# For DET view type
enabled_detection_models = [
    'efficientdet_d0.efficientnet_b0',
    'efficientdet_d1.efficientnet_b1',
    'efficientdet_d2.efficientnet_b2',
    'efficientdet_d3.efficientnet_b3',
    'efficientdet_d4.efficientnet_b4',
    'efficientdet_d5.efficientnet_b5',
    'faster_rcnn.resnet_101_v1',
    'faster_rcnn.resnet_50_v1',
    'ssd.inception_v2',
    'ssd.mobilenet_v1',
    'ssd.mobilenet_v2',
    'ssd_lite.mobilenet_v2',
    'yolo_v2.darknet_19',
    'yolo_v3.darknet_53',
    'yolo_v3_spp.darknet_53',
]


###############################################################################

form_parameters = {
    ViewType.CLASSIFICATION: (
        'image_classification.pretraining_natural_rgb.softmax.',
        enabled_classification_models,
        'efficientnet_b0'),

    ViewType.TAGGING: (
        'image_classification.pretraining_natural_rgb.sigmoid.',
        enabled_classification_models,
        'efficientnet_b0'),

    ViewType.DETECTION: (
        'image_detection.pretraining_natural_rgb.',
        enabled_detection_models,
        'efficientdet_d0.efficientnet_b0'),
}


###############################################################################

form = Form(form_parameters)


def num_train_steps_default_value(model_key, model, backend):
    """
    Yolo models have a large batch size (64) versus Tensorflow models (24 for SSD).
    To make training times comparable, we use a lower default number of iteration for
    Yolo.
    TODO: normalize batch sizes (64 in Yolo, 24 in TF detection) to make this comparable
    Args:
        model_key (str): the model key as in model_list.py
        model (ModelArguments): the corresponding ModelArguments instance
        backend (Backend): An instance of Backend
    Return:
        num_train_steps (int): the number of default training steps.
    """
    if backend == Backend.TENSORFLOW:
        return 20000
    elif backend == Backend.KERAS:
        return 20000
    elif backend == Backend.DARKNET:
        return 5000
    else:
        raise Exception('Unimplemented backend: {}'.format(backend))


only_for_tf_and_keras = DisplayCondition('backend', ['tensorflow', 'keras'])


# Training options
training_section = (
    Section('Training options')
    # Architecture
    .append(ModelControl('model', "Choose your architecture:"))
    # Number of train steps
    .append(InputControl(
        'trainer.num_train_steps',
        "The number of iterations:",
        min_value=10,
        max_value=10000000,
        increment_value=1000,
        # Callable default value: the value depends on the model
        default_value=num_train_steps_default_value))
    # Number of evaluation steps
    .append(InputControl(
        'evaluation.n_evaluations',
        "The number of evaluations:",
        min_value=0,
        max_value=100,
        increment_value=1,
        default_value=10,
        display_ifs=[only_for_tf_and_keras]))
    # Learning rate
    .append(InputControl(
        'trainer.initial_learning_rate',
        "Initial learning rate:",
        min_value=0,
        max_value=10,
        increment_value=0.0002)))
form.append(training_section)

# Optimizer options
optimizer_section = Section('Optimizer options', display_ifs=[only_for_tf_and_keras])
optimizer_section.append(
    SelectControl(
        'optimizer',
        'trainer.optimizer.optimizer',
        "Choose an optimizer:",
        [
            SelectOption('momentum_optimizer', 'Momentum Optimizer'),
            SelectOption('rms_prop_optimizer', 'RMS Prop Optimizer')
        ],
    )
)

# Momentum optimizer (only visible if momentum optimizer is selected)
condition = [DisplayCondition('optimizer', ['momentum_optimizer'])]
optimizer_section.append(
    InputControl(
        'trainer.optimizer.momentum_optimizer.momentum_optimizer_value',
        "Momentum value:",
        min_value=0,
        max_value=1,
        increment_value=0.05,
        display_ifs=condition
    )
)

# RMS Prop optimizer (only visible if rms prop optimizer is selected)
condition = [DisplayCondition('optimizer', ['rms_prop_optimizer'])]
optimizer_section.append(
    InputControl(
        'trainer.optimizer.rms_prop_optimizer.momentum_optimizer_value',
        "Momentum value:",
        min_value=0,
        max_value=1,
        increment_value=0.05,
        display_ifs=condition
    )
).append(
    InputControl(
        'trainer.optimizer.rms_prop_optimizer.decay',
        "Decay:",
        min_value=0,
        max_value=1,
        increment_value=0.05,
        display_ifs=condition
    )
).append(
    InputControl(
        'trainer.optimizer.rms_prop_optimizer.epsilon',
        "Espsilon:",
        min_value=0,
        max_value=1,
        increment_value=0.05,
        display_ifs=condition
    )
)
form.append(optimizer_section)

# Resize options
resizer_section = Section('Resizer image options', display_ifs=[])
resizer_section.append(
    SelectControl(
        'image_resizer',
        '@backbone.input.image_resizer.image_resizer_oneof',
        "Choose an image resizer type:",
        [
            SelectOption('fixed_shape_resizer', 'Fixed Shape Resizer'),
            SelectOption('keep_aspect_ratio_resizer', 'Keep Aspect Ratio Resizer', display_ifs=[only_for_tf_and_keras])
        ],
    )
)

# Width/Height (only visible if Fixed Shape Resizer is selected)
condition = [DisplayCondition('image_resizer', ['fixed_shape_resizer'])]
resizer_section.append(
    InputControl(
        '@backbone.input.image_resizer.fixed_shape_resizer.width',
        "Image width in pixels:",
        min_value=0,
        max_value=10000,
        increment_value=16,
        display_ifs=condition)
).append(
    InputControl(
        '@backbone.input.image_resizer.fixed_shape_resizer.height',
        "Image height in pixels:",
        min_value=0,
        max_value=10000,
        increment_value=16,
        display_ifs=condition))


# Image maximum (only visible if Keep Aspect Ratio Resizer is selected)
condition = [DisplayCondition('image_resizer', ['keep_aspect_ratio_resizer'])]
resizer_section.append(
    InputControl(
        '@backbone.input.image_resizer.keep_aspect_ratio_resizer.max_dimension',
        "Image maximum dimension in pixels:",
        min_value=0,
        max_value=10000,
        increment_value=1,
        display_ifs=condition
    )
)
form.append(resizer_section)


def add_class_balancing(protobuf, value):
    if is_true(value):
        protobuf.dataset.operations.append(dop.DataOperation(loss_based_balancing=dop.LossBasedBalancing()))


# Dataset options
dataset_section = (
    Section('Dataset options')
    .append(ToggleControl('balance', "Class balancing", default_value=False, protobuf_setter_fn=add_class_balancing))
    .append(InputControl(
        'dataset.margin_crop',
        "Crop margin:",
        min_value=0,
        max_value=1,
        increment_value=0.01,
        default_value=0))
)
form.append(dataset_section)
