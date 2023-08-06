# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Tab(Component):
    """A Tab component.
Tab component

Keyword arguments:

- children (list of a list of or a singular dash component, string or numbers | a list of or a singular dash component, string or number; optional):
    Tab content.

- id (string; optional):
    The ID of this component, used to identify dash components in
    callbacks. The ID needs to be unique across all of the components
    in an app.

- className (string; optional):
    Specify an optional className to be added to your Tab.

- disabled (boolean; optional):
    Whether your Tab is disabled.

- hidden (boolean; optional):
    Whether your Tab is disabled.

- label (string; required):
    Provide the contents of your Tab.

- role (string; optional):
    Provide an accessibility role for your Tab.

- style (dict; optional):
    jsx Style.

- value (string; optional):
    Value of the tab."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_carbon_components'
    _type = 'Tab'
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, className=Component.UNDEFINED, disabled=Component.UNDEFINED, hidden=Component.UNDEFINED, label=Component.REQUIRED, role=Component.UNDEFINED, value=Component.UNDEFINED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'className', 'disabled', 'hidden', 'label', 'role', 'style', 'value']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'className', 'disabled', 'hidden', 'label', 'role', 'style', 'value']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in ['label']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Tab, self).__init__(children=children, **args)
