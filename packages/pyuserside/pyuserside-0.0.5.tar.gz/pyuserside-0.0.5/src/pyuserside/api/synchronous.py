import requests
import json
from typing import Literal, Union, Optional, List, Any
from pyuserside.schema.device import DeviceData, DeviceDataWithIfaces
from pyuserside.schema.commutation import CommutationData, CommutationDataWithFinishData
from pyuserside.schema.customer import CustomerData
from pyuserside.schema.node import NodeData
import pyuserside.validators

class GenericUsersideCategory:
    def __init__(self, category: str, api: 'UsersideAPI'):
        self._api = api
        self._cat = category

    def __getattr__(self, action: str):
        def method(**kwargs):
            return self._api.request(cat=self._cat, action=action, **kwargs)
        return method


class Device(GenericUsersideCategory):
    def __init__(self, api: 'UsersideAPI'):
        super().__init__(category='device', api=api)

    def get_device_id(self, object_type: Literal['switch'],
                      data_typer: Literal['ip', 'mac', 'inventory_number', 'serial_number'],
                      data_value: str) -> int:
        params = {'object_type': object_type, 'data_typer': data_typer, 'data_value': data_value}
        pyuserside.validators.device.validate('get_device_id', **params)
        response = self._api.request(self._cat, 'get_device_id', **params)
        return response.get('id')

    def get_data(self, object_type: Literal['switch', 'onu', 'olt', 'radio', 'all'],
                 node_id: Optional[Union[str, int]] = None,
                 object_id: Optional[Union[str, int]] = None,
                 is_online: Optional[Union[str, int]] = None,
                 is_hide_ifaces_data: Optional[Union[str, int]] = None) -> List[DeviceData]:
        params = {'object_type': object_type,
                  'node_id': node_id,
                  'object_id': object_id,
                  'is_online': is_online,
                  'is_hide_ifaces_data': is_hide_ifaces_data}
        params = {k: v for k, v in params.items() if v}
        pyuserside.validators.device.validate('get_data', **params)
        response = self._api.request(self._cat, 'get_data', **params)
        response_class = DeviceData if is_hide_ifaces_data in [1, '1'] else DeviceDataWithIfaces
        return [response_class(**parameters) for parameters in response['data'].values()]


class Commutation(GenericUsersideCategory):
    def __init__(self, api: 'UsersideAPI'):
        super().__init__(category='commutation', api=api)

    def get_data(self, object_type: Literal['customer', 'switch', 'radio', 'cross', 'fiber', 'splitter'],
                 object_id: Optional[Union[int, str]] = None,
                 is_finish_data: Optional[Union[int, str]] = None):
        params = {'object_type': object_type,
                  'object_id': object_id,
                  'is_finish_data': is_finish_data}
        params = {k: v for k, v in params.items() if v}
        pyuserside.validators.commutation.validate('get_data', **params)
        response = self._api.request(self._cat, 'get_data', **params)
        response = response['data']
        response_class = CommutationDataWithFinishData if is_finish_data in [1, '1'] else CommutationData
        return response_class(response)

    def add(self, object_type: str = None,
            object_id: Union[int,str] = None,
            object1_side: Optional[Any] = None,
            object1_port: int = None,
            object2_type: str = None,
            object2_id: Union[int, str] = None,
            object2_side: Optional[Any] = None,
            object2_port: int = None):
        params = {'object_type': object_type,
                  'object_id': object_id,
                  'object1_side': object1_side,
                  'object1_port': object1_port,
                  'object2_type': object2_type,
                  'object2_id': object2_id,
                  'object2_side': object2_side,
                  'object2_port': object2_port
                  }
        params = {k: v for k, v in params.items() if v}
        pyuserside.validators.commutation.validate('add', **params)
        self._api.request(self._cat, 'add', **params)

    def delete(self, object_type: str, object_id: Union[str, int], object_port: Optional[Union[str, int]] = None):
        params = {'object_type': object_type,
                  'object_id': object_id,
                  'object_port': object_port,
                  }
        params = {k: v for k, v in params.items() if v}
        pyuserside.validators.commutation.validate('delete', **params)
        self._api.request(self._cat, 'delete', **params)


class Customer(GenericUsersideCategory):
    def __init__(self, api: 'UsersideAPI'):
        super().__init__('customer', api)

    def get_abon_id(self, data_typer: str, data_value: str, is_skip_old: Optional[Union[int, str]] = None):
        params = {'data_typer': data_typer,
                  'data_value': data_value,
                  'is_skip_old': is_skip_old,
                  }
        params = {k: v for k, v in params.items() if v}
        content = self._api.request(self._cat, 'get_abon_id', **params)
        if content.get('Result') == 'OK':
            return content.get('Id')
        else:
            raise ValueError('Customer was not found')

    def get_data(self, customer_id: Union[str, int]):
        params = {
            'customer_id': customer_id
        }
        content = self._api.request(self._cat, 'get_data', **params)
        return CustomerData(**content['data'])


class Node(GenericUsersideCategory):
    def __init__(self, api: 'UsersideAPI'):
        super().__init__('node', api)

    def get(self, address_id: Optional[Union[str, int]] = None, entrance_number: Optional[Union[str, int]] = None,
            house_id: Optional[Union[str, int]] = None, id: Optional[Union[str, int]] = None,
            mark_id: Optional[Union[str, int]] = None, object_type: Optional[Union[str, int]] = None,
            parent_id: Optional[Union[str, int]] = None):
        params = {'address_id': address_id,
                  'entrance_number': entrance_number,
                  'house_id': house_id,
                  'id': id,
                  'mark_id': mark_id,
                  'object_type': object_type,
                  'parent_id': parent_id,
                  }
        params = {k: v for k, v in params.items() if v}
        content = self._api.request(self._cat, 'get', **params)
        return [NodeData(**parameters) for parameters in content['data'].values()]


class UsersideAPI:
    def __init__(self, url: str, key: str):
        self._url = url
        self._key = key
        self._session = None
        self.device = Device(self)
        self.commutation = Commutation(self)
        self.customer = Customer(self)
        self.node = Node(self)

    def __getattr__(self, item):
        return GenericUsersideCategory(item, self)

    def request(self, cat: str, action: str, **kwargs) -> dict:
        close_after_request = False
        if not self._session:
            self._session = requests.Session()
            close_after_request = True
        params = {'key': self._key, 'cat': cat, 'action': action}
        params.update(kwargs)
        response = self._session.get(url=self._url, params=params)
        success = True
        answer = ''
        error_message = ''
        if not response.content:
            success = False
            error_message = 'Empty response'
        elif not response.ok:
            success = False
            error_message = response.content.decode('utf-8')
        else:
            answer = json.loads(response.content.decode('utf-8'))
        if close_after_request:
            self._session.close()
            self._session = None
        if not success:
            raise requests.HTTPError(error_message)
        return answer

    def __enter__(self):
        self._session = requests.Session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._session.close()
        self._session = None
