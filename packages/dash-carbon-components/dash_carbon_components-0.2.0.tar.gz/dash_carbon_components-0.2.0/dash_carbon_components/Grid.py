# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Grid(Component):
    """A Grid component.
Carbon Grid

Keyword arguments:

- children (list of a list of or a singular dash component, string or numbers | a list of or a singular dash component, string or number; optional):
    The children of the element.

- id (string; optional):
    The ID of this component, used to identify dash components in
    callbacks. The ID needs to be unique across components in an app.

- className (string; default ''):
    The class of the element.

- condensed (boolean; optional):
    Collapse the gutter to 1px. Useful for fluid layouts. Rows have
    1px of margin between them to match gutter.

- fullWidth (boolean; optional):
    Remove the default max width that the grid has set.

- narrow (boolean; optional):
    Container hangs 16px into the gutter. Useful for typographic
    alignment with and without containers.

- style (dict; optional):
    The inline styles."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_carbon_components'
    _type = 'Grid'
    @_explicitize_args
    def __init__(self, children=None, style=Component.UNDEFINED, id=Component.UNDEFINED, className=Component.UNDEFINED, condensed=Component.UNDEFINED, fullWidth=Component.UNDEFINED, narrow=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'className', 'condensed', 'fullWidth', 'narrow', 'style']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'className', 'condensed', 'fullWidth', 'narrow', 'style']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Grid, self).__init__(children=children, **args)
