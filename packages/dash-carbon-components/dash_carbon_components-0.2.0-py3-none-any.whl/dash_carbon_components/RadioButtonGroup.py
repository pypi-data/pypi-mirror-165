# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class RadioButtonGroup(Component):
    """A RadioButtonGroup component.
Radio Group Component

Keyword arguments:

- id (string; optional):
    Specify a custom `id` for the radio group.

- className (string; optional):
    Provide an optional className to be applied to the container node.

- disabled (boolean; optional):
    Specify whether the group is disabled.

- labelPosition (a value equal to: 'left', 'right'; optional):
    Provide where label text should be placed.

- legendText (a list of or a singular dash component, string or number; optional):
    Provide a legend to the RadioButtonGroup input that you are
    exposing to the user.

- orientation (a value equal to: 'horizontal', 'vertical'; optional):
    Provide where radio buttons should be placed.

- radiosButtons (list of dicts; optional):
    The radios buttons inside this group.

    `radiosButtons` is a list of dicts with keys:

    - id (string; optional)

    - label (string; optional)

    - value (string; optional)

- style (dict; optional):
    jsx Style.

- value (string; optional):
    The value selected."""
    _children_props = ['legendText']
    _base_nodes = ['legendText', 'children']
    _namespace = 'dash_carbon_components'
    _type = 'RadioButtonGroup'
    @_explicitize_args
    def __init__(self, legendText=Component.UNDEFINED, radiosButtons=Component.UNDEFINED, id=Component.UNDEFINED, value=Component.UNDEFINED, labelPosition=Component.UNDEFINED, orientation=Component.UNDEFINED, disabled=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'className', 'disabled', 'labelPosition', 'legendText', 'orientation', 'radiosButtons', 'style', 'value']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'className', 'disabled', 'labelPosition', 'legendText', 'orientation', 'radiosButtons', 'style', 'value']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(RadioButtonGroup, self).__init__(**args)
