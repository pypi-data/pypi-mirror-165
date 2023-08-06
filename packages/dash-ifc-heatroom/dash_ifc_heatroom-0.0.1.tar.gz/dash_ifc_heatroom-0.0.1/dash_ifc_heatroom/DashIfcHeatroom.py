# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DashIfcHeatroom(Component):
    """A DashIfcHeatroom component.


Keyword arguments:

- id (string; required):
    The ID used to identify the container for the IFC viewer
    component.

- ifcData (string; optional):
    The contents of the ifc file."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_ifc_heatroom'
    _type = 'DashIfcHeatroom'
    @_explicitize_args
    def __init__(self, id=Component.REQUIRED, ifcData=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'ifcData']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'ifcData']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in ['id']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(DashIfcHeatroom, self).__init__(**args)
