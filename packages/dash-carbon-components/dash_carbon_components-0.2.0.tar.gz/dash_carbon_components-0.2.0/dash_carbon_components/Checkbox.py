# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Checkbox(Component):
    """A Checkbox component.
Checkbox Input

Keyword arguments:

- id (string; required):
    Provide an `id` to uniquely identify the Checkbox input.

- className (string; optional):
    Specify an optional className to be applied to the <label> node.

- disabled (boolean; optional):
    Specify whether the Checkbox should be disabled.

- hideLabel (boolean; optional):
    Specify whether the label should be hidden, or not.

- label (a list of or a singular dash component, string or number; required):
    Provide a label to provide a description of the Checkbox input
    that you are exposing to the user.

- style (dict; optional):
    The inline styles.

- title (string; optional):
    Specify a title for the <label> node for the Checkbox.

- value (boolean; optional):
    Specify whether the underlying input is checked."""
    _children_props = ['label']
    _base_nodes = ['label', 'children']
    _namespace = 'dash_carbon_components'
    _type = 'Checkbox'
    @_explicitize_args
    def __init__(self, id=Component.REQUIRED, label=Component.REQUIRED, hideLabel=Component.UNDEFINED, disabled=Component.UNDEFINED, value=Component.UNDEFINED, title=Component.UNDEFINED, style=Component.UNDEFINED, className=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'className', 'disabled', 'hideLabel', 'label', 'style', 'title', 'value']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'className', 'disabled', 'hideLabel', 'label', 'style', 'title', 'value']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in ['id', 'label']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Checkbox, self).__init__(**args)
