def validate(method: str, **params):
    if method == 'get_data':
        return get_data(**params)
    elif method == 'add':
        return add(**params)
    elif method == 'delete':
        return delete(**params)


def get_data(**params):
    if 'object_type' not in params:
        raise KeyError('object_type missing')
    if params.get('object_type') not in ['customer', 'switch', 'radio', 'cross', 'fiber', 'splitter']:
        raise ValueError('object_type must be on of the following: customer, switch, radio, cross, fiber, splitter')
    is_finish_data = params.get('is_finish_data')
    if (is_finish_data) and (is_finish_data not in [1, '1']):
        raise RuntimeWarning('is_finish_data must be 1 to take effect, but now it is {}'.format(is_finish_data))


def add(**params):
    if 'object_type' not in params:
        raise KeyError('object_type missing')
    if params.get('object_type') not in ['customer', 'switch', 'fiber', 'cross']:
        raise ValueError('object_type must be on of the following: customer, switch, fiber, cross')
    if 'object_id' not in params:
        raise KeyError('object_id missing')
    if params.get('object_type') == 'fiber':
        if 'object1_side' not in params:
            raise KeyError('object1_side missing')
    else:
        if 'object1_side' in params:
            raise RuntimeWarning('object1_side parameter is using only when connect fiber devices')
    if 'object1_port' not in params:
        raise KeyError('object1_port missing')
    if 'object2_type' not in params:
        raise KeyError('object2_type missing')
    if params.get('object2_type') not in ['switch', 'fiber', 'cross']:
        raise ValueError('object2_type must be on of the following: switch, fiber, cross')
    if 'object2_id' not in params:
        raise KeyError('object2_id missing')
    if params.get('object2_type') == 'fiber':
        if 'object2_side' not in params:
            raise KeyError('object2_side missing')
    else:
        if 'object2_side' in params:
            raise RuntimeWarning('object2_side parameter is using only when connect fiber devices')
    if 'object2_port' not in params:
        raise KeyError('object2_port missing')


def delete(**params):
    if 'object_type' not in params:
        raise KeyError('object_type missing')
    if 'object_id' not in params:
        raise KeyError('object_id missing')


