# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DatePickerRange(Component):
    """A DatePickerRange component.
DatePickerRange, the id of the DateInputs will be id + '-start' and id + '-end'

Keyword arguments:

- id (string; required):
    The ID of this component, used to identify dash components in
    callbacks. The ID needs to be unique across all of the components
    in an app.

- dateFormat (string; optional):
    The date format.

- endLabel (string; required):
    End input label.

- light (boolean; optional):
    True to use the light version.

- locale (string; optional):
    The language locale used to format the days of the week, months,
    and numbers. The full list of supported locales can be found here
    https://github.com/flatpickr/flatpickr/tree/master/src/l10n.

- maxDate (string; optional):
    The maximum date that a user can pick to.

- minDate (string; optional):
    The minimum date that a user can start picking from.

- placeholder (string; required):
    placeholder.

- short (boolean; optional):
    True to use the short version.

- startLabel (string; required):
    Start input label.

- style (dict; optional):
    jsx Style.

- value (string | list of strings; optional):
    The value of the date value provided to flatpickr."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_carbon_components'
    _type = 'DatePickerRange'
    @_explicitize_args
    def __init__(self, id=Component.REQUIRED, dateFormat=Component.UNDEFINED, light=Component.UNDEFINED, locale=Component.UNDEFINED, maxDate=Component.UNDEFINED, minDate=Component.UNDEFINED, short=Component.UNDEFINED, value=Component.UNDEFINED, startLabel=Component.REQUIRED, endLabel=Component.REQUIRED, placeholder=Component.REQUIRED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'dateFormat', 'endLabel', 'light', 'locale', 'maxDate', 'minDate', 'placeholder', 'short', 'startLabel', 'style', 'value']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'dateFormat', 'endLabel', 'light', 'locale', 'maxDate', 'minDate', 'placeholder', 'short', 'startLabel', 'style', 'value']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in ['id', 'endLabel', 'placeholder', 'startLabel']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(DatePickerRange, self).__init__(**args)
