# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Slider(Component):
    """A Slider component.
Slider

Keyword arguments:

- id (string; optional):
    The ID of this component, used to identify dash components in
    callbacks. The ID needs to be unique across all of the components
    in an app.

- ariaLabelInput (string; optional):
    The ARIA label for the <input>.

- disabled (boolean; default False):
    Disabled.

- hideTextInput (boolean; default False):
    Without text input.

- inputType (string; default 'number'):
    The form element type.

- labelText (string; required):
    Label text.

- light (boolean; default False):
    Light variant.

- max (number; required):
    The maximum value.

- min (number; required):
    The minimum value.

- name (string; optional):
    Form item name.

- step (number; required):
    The step.

- stepMultiplier (number; default 5):
    The step factor for Shift+arrow keys.

- style (dict; optional):
    jsx Style.

- value (number; required):
    The value."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_carbon_components'
    _type = 'Slider'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, name=Component.UNDEFINED, inputType=Component.UNDEFINED, ariaLabelInput=Component.UNDEFINED, labelText=Component.REQUIRED, disabled=Component.UNDEFINED, light=Component.UNDEFINED, hideTextInput=Component.UNDEFINED, value=Component.REQUIRED, min=Component.REQUIRED, max=Component.REQUIRED, step=Component.REQUIRED, stepMultiplier=Component.UNDEFINED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'ariaLabelInput', 'disabled', 'hideTextInput', 'inputType', 'labelText', 'light', 'max', 'min', 'name', 'step', 'stepMultiplier', 'style', 'value']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'ariaLabelInput', 'disabled', 'hideTextInput', 'inputType', 'labelText', 'light', 'max', 'min', 'name', 'step', 'stepMultiplier', 'style', 'value']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in ['labelText', 'max', 'min', 'step', 'value']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Slider, self).__init__(**args)
