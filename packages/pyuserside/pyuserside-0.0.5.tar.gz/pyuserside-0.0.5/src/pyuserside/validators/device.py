def validate(method: str, **params):
    if method == 'get_device_id':
        return validate_get_device_id(**params)
    elif method == 'get_data':
        return validate_get_data(**params)


def validate_get_device_id(**params):
    if 'object_type' not in params:
        raise KeyError('object_type missing')
    if params.get('object_type') not in ['switch']:
        raise ValueError('object_type must be on of the following: switch')
    if 'data_typer' not in params:
        raise KeyError('data_typer missing')
    if params.get('data_typer') not in ['ip', 'mac', 'inventory_number', 'serial_number']:
        raise ValueError('object_type must be on of the following: ip, mac, inventory_number, serial_number')
    if 'data_value' not in params:
        raise KeyError('data_value missing')
    extra_keys = [key for key in params.keys() if key not in ['object_type', 'data_typer', 'data_value']]
    if extra_keys:
        raise AttributeError('Unrecognized parameters: {}'.format(', '.join(extra_keys)))


def validate_get_data(**params):
    if 'object_type' not in params:
        raise KeyError('object_type missing')
    if params.get('object_type') not in ['switch', 'onu', 'olt', 'radio', 'all']:
        raise ValueError('object_type must be on of the following: switch, onu, olt, radio, all')
    is_hide_ifaces_data = params.get('is_hide_ifaces_data')
    if (is_hide_ifaces_data) and (is_hide_ifaces_data not in [1, '1']):
        raise RuntimeWarning('is_hide_ifaces_data must be 1 to take effect, now it is {}'.format(is_hide_ifaces_data))
