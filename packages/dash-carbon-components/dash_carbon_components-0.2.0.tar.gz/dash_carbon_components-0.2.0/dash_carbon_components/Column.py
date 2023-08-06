# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Column(Component):
    """A Column component.
Row Column

Keyword arguments:

- children (list of a list of or a singular dash component, string or numbers | a list of or a singular dash component, string or number; optional):
    The children of the element.

- id (string; optional):
    The ID of this component, used to identify dash components in
    callbacks. The ID needs to be unique across all of the components
    in an app.

- className (string; default ''):
    Specify a custom className to be applied to the `Column`.

- lg (optional):
    Specify column span for the `lg` breakpoint (Default breakpoint up
    to 1312px) This breakpoint supports 16 columns by default.  @see
    https://www.carbondesignsystem.com/guidelines/layout#breakpoints.

- max (optional):
    Specify column span for the `max` breakpoint. This breakpoint
    supports 16 columns by default.  @see
    https://www.carbondesignsystem.com/guidelines/layout#breakpoints.

- md (optional):
    Specify column span for the `md` breakpoint (Default breakpoint up
    to 1056px) This breakpoint supports 8 columns by default.  @see
    https://www.carbondesignsystem.com/guidelines/layout#breakpoints.

- sm (optional):
    Specify column span for the `sm` breakpoint (Default breakpoint up
    to 672px) This breakpoint supports 4 columns by default.  @see
    https://www.carbondesignsystem.com/guidelines/layout#breakpoints.

- style (dict; optional):
    The inline styles.

- xlg (optional):
    Specify column span for the `xlg` breakpoint (Default breakpoint
    up to 1584px) This breakpoint supports 16 columns by default.
    @see
    https://www.carbondesignsystem.com/guidelines/layout#breakpoints."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_carbon_components'
    _type = 'Column'
    @_explicitize_args
    def __init__(self, children=None, style=Component.UNDEFINED, id=Component.UNDEFINED, className=Component.UNDEFINED, lg=Component.UNDEFINED, max=Component.UNDEFINED, md=Component.UNDEFINED, sm=Component.UNDEFINED, xlg=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'className', 'lg', 'max', 'md', 'sm', 'style', 'xlg']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'className', 'lg', 'max', 'md', 'sm', 'style', 'xlg']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Column, self).__init__(children=children, **args)
