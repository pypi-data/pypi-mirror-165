# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Dropdown(Component):
    """A Dropdown component.
Dropdown component

Keyword arguments:

- id (string; required):
    Specify a custom `id`.

- ariaLabel (string; optional):
    'aria-label' of the ListBox component.

- disabled (boolean; optional):
    Disable the control.

- helperText (string | a list of or a singular dash component, string or number; optional):
    Provide helper text that is used alongside the control label for
    additional help.

- inline (boolean; optional):
    Specify whether you want the inline version of this control.

- invalid (boolean; optional):
    Specify if the currently selected value is invalid.

- invalidText (string; optional):
    Message which is displayed if the value is invalid.

- label (a list of or a singular dash component, string or number; required):
    Generic `label` that will be used as the textual representation of
    what this field is for.

- light (boolean; optional):
    `True` to use the light version.

- options (list of dicts; optional):
    List of items.

    `options` is a list of string | dict with keys:

    - label (string; optional)

    - value (boolean | number | string | dict | list; optional)s

- style (dict; optional):
    Style of the component.

- titleText (string | a list of or a singular dash component, string or number; optional):
    Provide the title text that will be read by a screen reader when
    visiting this control.

- value (boolean | number | string | dict | list; optional):
    In the case you want to control the dropdown selection entirely."""
    _children_props = ['label', 'titleText', 'helperText']
    _base_nodes = ['label', 'titleText', 'helperText', 'children']
    _namespace = 'dash_carbon_components'
    _type = 'Dropdown'
    @_explicitize_args
    def __init__(self, disabled=Component.UNDEFINED, options=Component.UNDEFINED, id=Component.REQUIRED, inline=Component.UNDEFINED, invalid=Component.UNDEFINED, invalidText=Component.UNDEFINED, label=Component.REQUIRED, translateWithId=Component.UNDEFINED, ariaLabel=Component.UNDEFINED, value=Component.UNDEFINED, light=Component.UNDEFINED, titleText=Component.UNDEFINED, helperText=Component.UNDEFINED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'ariaLabel', 'disabled', 'helperText', 'inline', 'invalid', 'invalidText', 'label', 'light', 'options', 'style', 'titleText', 'value']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'ariaLabel', 'disabled', 'helperText', 'inline', 'invalid', 'invalidText', 'label', 'light', 'options', 'style', 'titleText', 'value']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in ['id', 'label']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Dropdown, self).__init__(**args)
