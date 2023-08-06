# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class UIShell(Component):
    """An UIShell component.
UIShell is a default layout with the header and a sidebar

Keyword arguments:

- id (string; optional):
    Element id.

- headerItems (list of dicts; optional):
    Items of the header.

    `headerItems` is a list of dicts with keys:

    - name (string; optional)

    - url (string; optional)

- loading_state (dict; optional):
    Object that holds the loading state object coming from
    dash-renderer.

    `loading_state` is a dict with keys:

    - component_name (string; optional):
        Holds the name of the component that is loading.

    - is_loading (boolean; optional):
        Determines if the component is loading or not.

    - prop_name (string; optional):
        Holds which property is loading.

- name (string; required):
    Platform Name.

- sidebarItems (list of dicts; optional):
    Items of the sidebar.

    `sidebarItems` is a list of dicts with keys:

    - name (string; optional)

    - url (string; optional)"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_carbon_components'
    _type = 'UIShell'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, name=Component.REQUIRED, sidebarItems=Component.UNDEFINED, headerItems=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'headerItems', 'loading_state', 'name', 'sidebarItems']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'headerItems', 'loading_state', 'name', 'sidebarItems']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in ['name']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(UIShell, self).__init__(**args)
