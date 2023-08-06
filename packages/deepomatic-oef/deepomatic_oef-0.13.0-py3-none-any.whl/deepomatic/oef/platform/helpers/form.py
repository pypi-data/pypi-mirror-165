import copy
import json
from google.protobuf.message import Message
from typing import Dict, List, Tuple

from deepomatic.oef.configs.model_list import model_list
from deepomatic.oef.utils.experiment_builder import ExperimentBuilder

from .common import BACKEND_FILE
from .controls import Control, ControlType, ModelControl, SelectOption, SelectControl, ToggleControl, DisplayCondition
from .tags import Tags, Backend, ViewType


###############################################################################

class Form(Control):
    """
    Use this class to regroup all the sections of the training form and generate JSON.
    """

    def __init__(self, padding_left: int = 0, display_ifs: List[DisplayCondition] = None):
        """
        Create a Form which is used to wrap a list of controls. Left padding
        can be applied to all wrapped controls to visually create an impression
        of hierachy between a control and its sub-controls.

        Args:
            padding_left (int): The left padding in pixels
            display_ifs (list): A list of DisplayCondition

        Return:
            The Control object.
        """
        super().__init__(None, None, None, ControlType.FORM, None, None, display_ifs=display_ifs)
        self._controls = []
        self._padding_left = padding_left

    @property
    def controls(self):
        return self._controls

    def append(self, control: Control):
        self._controls.append(control)
        return self

    def json(self):
        """
        Convert the object into a Python dict which is JSON-serializable.
        """
        return {
            'type': 'form',
            'display_if': [d.json() for d in self._display_ifs],
            'padding_left': self._padding_left,
            'controls': [control.json() for control in self._controls],
        }

    def parse_tags(self, payload: dict, tags: Dict[str, str]):
        for control in self._controls:
            if isinstance(control, Form):
                control.parse_tags(payload, tags)
                continue

            elif control.property_name is None:
                continue

            # Do not remove this sanity check: it allows to make sure
            # the test payloads are up-to-date
            if control.property_name not in payload:
                raise Exception(f"Missing value: {control.property_name}")
            value = payload[control.property_name]

            if control.value_to_tag_map is not None:
                if isinstance(value, bool):
                    # Boolean value will be silently dumped as "true" and "false" in the
                    # JSON default_models.json.
                    tags.update(control.value_to_tag_map[str(value).lower()])
                else:
                    tags.update(control.value_to_tag_map[value])

            if isinstance(control, (SelectControl, ToggleControl)):
                tags[control.property_name] = value

    def parse_payload(self, protobuf: Message, payload: dict, tags: Dict[str, str], parent_visible: bool = True):
        is_visible = parent_visible and self.is_visible(tags)
        for control in self._controls:
            if isinstance(control, Form):
                control.parse_payload(protobuf, payload, tags, is_visible)
                continue

            elif control.property_name is None or isinstance(control, ModelControl):
                continue  # This is the model select, we already used its value

            # We make sure we pop the values even if the form is not visible
            value = payload.pop(control.property_name)
            if is_visible and control.is_visible(tags):
                control.protobuf_setter_fn(protobuf, value)

    def get_form_default_values(self, model_key, xp, backend):
        default_values = {}
        for control in self._controls:
            if isinstance(control, Form):
                default_values.update(control.get_form_default_values(model_key, xp, backend))
            else:
                if control.property_name is None:
                    continue
                value = control.default_value(model_key, xp, backend)
                if value is None:
                    continue
                default_values[control.property_name] = value
        return default_values


###############################################################################

class MainForm(Form):

    """
    Use this class to regroup all the sections of the training form and generate JSON.
    """

    def __init__(self, enabled_models_per_view: Dict[ViewType, Tuple[str, List[str], str]]):
        """
        Args:
            form_parameters (dict): dict from ViewType to 3-tuple (model_prefix, [model_key], default_model)
        """
        super().__init__()

        self._enabled_models = {}
        self._default_models = {}
        for view_type, (model_prefix, enabled_models, default_model) in enabled_models_per_view.items():
            self._enabled_models[view_type] = [model_prefix + m for m in enabled_models]
            self._default_models[view_type] = model_prefix + default_model
            assert self._default_models[view_type] in self._enabled_models[view_type], 'Could not find default model: {} in [{}]'.format(self._default_models[view_type], self._enabled_models[view_type])

        # Load the backend map
        with open(BACKEND_FILE, 'r') as f:
            self._backends = {k: Backend(v) for k, v in json.load(f).items()}

    def append(self, control: Control):
        super().append(control)

        # The values for the model control must be accumulated at built time
        # for the parse function to work.
        if isinstance(control, ModelControl):
            for view_type in self._enabled_models:
                # Compute model select values and tags
                model_select_values = []
                model_select_tags = {}
                for model_key in self._enabled_models[view_type]:
                    model_select_values.append(
                        SelectOption(
                            model_key,
                            model_list[model_key].display_name
                        )
                    )
                    model_select_tags[model_key] = Tags([self._backends[model_key]])

                # Set available models
                control.set_values_and_tags(view_type, model_select_values, model_select_tags)

        return self

    def json(self):
        """
        Return JSON describing the form to display in Vesta's front-end.
        See README.md for a description of the format.

        Return:
            The JSON that fully describe the training form in Vesta
        """
        # Sanity check:
        properties = set()
        for control in self._controls:
            if control.property_name is not None:
                if control.property_name in properties:
                    raise Exception('Property already exists: {}'.format(control.property_name))
                properties.add(control.property_name)

        model_control = self._get_model_control_()

        json_payload = {}
        # Generate the value_to_tag_map for all models
        model_property_name = model_control.property_name
        for view_type in self._enabled_models:
            # Set available models
            model_control.select_view_type(view_type)
            json_payload[view_type.value] = {
                'model_property_name': model_property_name,
                'default_model': self._default_models[view_type],
                'form': super().json(),
                'default_values': {
                    model_key: self._model_json_(model_key, self._backends[model_key])
                    for model_key in self._enabled_models[view_type]
                }
            }

        # Some dictionary keys may be booleans (which is not JSON compatible):
        # by dumping and reloading to json, we ensure a json compatible format.
        # Booleans are converted to 'false' or 'true' when used in dict keys.
        return json.loads(json.dumps(json_payload))

    def _get_model_control_(self):
        model_control = None
        for control in self._controls:
            if isinstance(control, ModelControl):
                if model_control is not None:
                    raise Exception("There can be only one ModelControl in the form")
                model_control = control
        if model_control is None:
            raise Exception("Model not found")
        return model_control

    def _model_json_(self, model_key: str, backend: Backend):
        """
        A helper function to build the JSON that describes the default values of a given `model_key`.

        Args:
            model_key (str): a default model key like 'image_classification.pretraining_natural_rgb.sigmoid.efficientnet_b0'
            backend: An instance of Backend

        Return:
            The JSON that fully describe the default values for this model.
        """
        builder = ExperimentBuilder(model_key)
        xp = builder.build()
        return self.get_form_default_values(model_key, xp, backend)

    def parse(self, payload: dict):
        """
        Convert a API POST request into an experiment protobuf
        """
        payload = copy.deepcopy(payload)

        # Set enabled tags
        tags = {}
        self.parse_tags(payload, tags)

        # Build protobuf
        model_control = self._get_model_control_()
        model_key = payload.pop(model_control.property_name)
        experiment = ExperimentBuilder(model_key).build()

        # Once all the tags are set, we can safely decide which controls are visible
        self.parse_payload(experiment, payload, tags)

        # Do not remove this sanity check: it allows to make sure
        # the test payloads are up-to-date
        if len(payload) > 0:
            raise Exception(f"Unknown values: {', '.join(payload.keys())}")

        return experiment
