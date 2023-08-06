# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Tabs(Component):
    """A Tabs component.
Tabs

Keyword arguments:

- children (list of a list of or a singular dash component, string or numbers | a list of or a singular dash component, string or number; optional):
    Pass in a collection of <Tab> children to be rendered depending on
    the currently selected tab.

- id (string; optional):
    The ID of this component, used to identify dash components in
    callbacks. The ID needs to be unique across all of the components
    in an app.

- ariaLabel (string; optional):
    Specify the text to be read by screen-readers when visiting the
    <Tabs> component.

- className (string; optional):
    Provide a className that is applied to the root <nav> component
    for the <Tabs>.

- headerOffsets (list of strings; optional):
    Number of columns of left offset the header will have.

- headerSizes (list of strings; optional):
    Number of columns the header will have.

- hidden (boolean; optional):
    Specify whether the Tab content is hidden.

- iconDescription (string; default 'show menu options'):
    Provide a description that is read out when a user visits the
    caret icon for the dropdown menu of items.

- role (string; default 'navigation'):
    By default, this value is \"navigation\". You can also provide an
    alternate role if it makes sense from the accessibility-side.

- selected (number; optional):
    Optionally provide an index for the currently selected <Tab>.

- style (dict; optional):
    Specify the inline style.

- tabContentClassName (string; optional):
    Provide a className that is applied to the <TabContent>
    components.

- triggerHref (string; default '#'):
    Provide a string that represents the `href` for the triggered
    <Tab>.

- value (string; optional):
    Value of the selected tab."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_carbon_components'
    _type = 'Tabs'
    @_explicitize_args
    def __init__(self, children=None, ariaLabel=Component.UNDEFINED, style=Component.UNDEFINED, className=Component.UNDEFINED, hidden=Component.UNDEFINED, role=Component.UNDEFINED, onClick=Component.UNDEFINED, onKeyDown=Component.UNDEFINED, triggerHref=Component.UNDEFINED, selected=Component.UNDEFINED, iconDescription=Component.UNDEFINED, tabContentClassName=Component.UNDEFINED, id=Component.UNDEFINED, headerOffsets=Component.UNDEFINED, headerSizes=Component.UNDEFINED, value=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'ariaLabel', 'className', 'headerOffsets', 'headerSizes', 'hidden', 'iconDescription', 'role', 'selected', 'style', 'tabContentClassName', 'triggerHref', 'value']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'ariaLabel', 'className', 'headerOffsets', 'headerSizes', 'hidden', 'iconDescription', 'role', 'selected', 'style', 'tabContentClassName', 'triggerHref', 'value']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Tabs, self).__init__(children=children, **args)
