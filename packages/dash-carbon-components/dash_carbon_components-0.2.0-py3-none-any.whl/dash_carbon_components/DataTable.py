# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DataTable(Component):
    """A DataTable component.
DataTable

Keyword arguments:

- id (string; required):
    The ID of this component, used to identify dash components in
    callbacks. The ID needs to be unique across all of the components
    in an app.

- action (dict; optional):
    Output only, this prop will be updated every time the user press
    one action.

    `action` is a dict with keys:

    - id (string; optional)

    - timestamp (string; optional)

- actions (list of dicts; optional):
    List of custom actions avaible in this table, every time the user
    press in one of the actions the action prop will be updated with
    the id of the action and the time of the click.

    `actions` is a list of dicts with keys:

    - id (string; optional)

    - name (string; optional)

- centerElements (boolean; default False)

- className (string; optional)

- columns (list of dicts; optional):
    True to use the light version.

    `columns` is a list of dicts with keys:

    - id (string; optional)

    - name (string; optional)

- data (list; optional):
    The date format.

- description (string; optional):
    Description of the table.

- iconColumns (list; optional)

- isPageable (boolean; optional):
    Whether to paginate the table.

- isSearchable (boolean; optional):
    Whether the table should have the search input.

- isSortable (boolean; optional):
    Specify whether the table should be able to be sorted by its
    headers.

- locale (string; optional):
    Provide a string for the current locale.

- overflowMenuOnHover (boolean; optional):
    Specify whether the overflow menu (if it exists) should be shown
    always, or only on hover.

- pageSize (number; optional)

- pageSizes (list of dicts; default [    {text: 'Ten', value: 10},    {text: 'Twenty', value: 20},    {text: 'Thirty', value: 30},    {text: 'Fourty', value: 40},    {text: 'Fifty', value: 50},])

    `pageSizes` is a list of dicts with keys:

    - text (string; optional)

    - value (number; optional)

- radio (boolean; optional):
    Specify whether the control should be a radio button or inline
    checkbox.

- shouldShowBorder (boolean; optional):
    `False` If True, will remove the table border.

- size (a value equal to: 'xs', 'sm', 'md', 'lg', 'xl'; optional):
    Change the row height of table. Currently supports `xs`, `sm`,
    `md`, `lg`, and `xl`.

- stickyHeader (boolean; optional):
    Specify whether the header should be sticky. Still experimental:
    may not work with every combination of table props.

- style (dict; optional):
    jsx Style.

- title (string; optional):
    Title of the table.

- useStaticWidth (boolean; optional):
    `False` If True, will use a width of 'auto' instead of 100%.

- useZebraStyles (boolean; optional):
    `True` to add useZebraStyles striping."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_carbon_components'
    _type = 'DataTable'
    @_explicitize_args
    def __init__(self, className=Component.UNDEFINED, id=Component.REQUIRED, data=Component.UNDEFINED, columns=Component.UNDEFINED, isSortable=Component.UNDEFINED, locale=Component.UNDEFINED, overflowMenuOnHover=Component.UNDEFINED, radio=Component.UNDEFINED, shouldShowBorder=Component.UNDEFINED, size=Component.UNDEFINED, stickyHeader=Component.UNDEFINED, useStaticWidth=Component.UNDEFINED, useZebraStyles=Component.UNDEFINED, title=Component.UNDEFINED, description=Component.UNDEFINED, isSearchable=Component.UNDEFINED, actions=Component.UNDEFINED, action=Component.UNDEFINED, isPageable=Component.UNDEFINED, pageSizes=Component.UNDEFINED, pageSize=Component.UNDEFINED, style=Component.UNDEFINED, centerElements=Component.UNDEFINED, iconColumns=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'action', 'actions', 'centerElements', 'className', 'columns', 'data', 'description', 'iconColumns', 'isPageable', 'isSearchable', 'isSortable', 'locale', 'overflowMenuOnHover', 'pageSize', 'pageSizes', 'radio', 'shouldShowBorder', 'size', 'stickyHeader', 'style', 'title', 'useStaticWidth', 'useZebraStyles']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'action', 'actions', 'centerElements', 'className', 'columns', 'data', 'description', 'iconColumns', 'isPageable', 'isSearchable', 'isSortable', 'locale', 'overflowMenuOnHover', 'pageSize', 'pageSizes', 'radio', 'shouldShowBorder', 'size', 'stickyHeader', 'style', 'title', 'useStaticWidth', 'useZebraStyles']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in ['id']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(DataTable, self).__init__(**args)
