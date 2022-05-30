import uuid

from base.api.users.datagrid_settings.datagrid_settings import get_data_grid_settings, get_data_grid_setting, \
    create_data_grid_setting, delete_data_grid_setting

data_grid_settings_methods = [
    {
        'method': get_data_grid_settings,
        'args': (),
        'key': 'data_grid_settings.get_data_grid_settings'
    },
    {
        'method': get_data_grid_setting,
        'args': ('some_key',),
        'key': 'data_grid_settings.get_data_grid_setting'
    },
    {
        'method': create_data_grid_setting,
        'args': ({},),
        'key': 'data_grid_settings.create_data_grid_setting'
    },
    {
        'method': delete_data_grid_setting,
        'args': (uuid.uuid4(),),
        'key': 'data_grid_settings.delete_data_grid_setting'
    },
]
