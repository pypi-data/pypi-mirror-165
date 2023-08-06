from pprint import pprint
import json
from typing import Literal, Union, Optional, List, Any, Type
import aiohttp
from pyuserside.schema.device import DeviceData, DeviceDataWithIfaces
from pyuserside.schema.commutation import CommutationData, CommutationDataWithFinishData
from pyuserside.schema.customer import CustomerData
from pyuserside.schema.node import NodeData
from pyuserside.schema.task import TaskData
import pyuserside.validators


class GenericUsersideCategory:
    """Base category. No validation, no response model, no typehints

    :type category: str
    :param category: Category name

    :type api: :class:`pyuserside.asynchronous.UsersideAPI`
    :param api: UsersideAPI object to use as parent
    """
    def __init__(self, category: str, api: 'UsersideAPI'):
        self._api = api
        self._cat = category

    def __getattr__(self, action: str):
        """Dynamic method creation

        :type action: str
        :param action: Method name
        """
        async def method(**kwargs):
            return await self._api.request(cat=self._cat, action=action, **kwargs)
        return method


class Device(GenericUsersideCategory):
    def __init__(self, api: 'UsersideAPI'):
        super().__init__(category='device', api=api)

    async def get_device_id(self, object_type: Literal['switch'],
                            data_typer: Literal['ip', 'mac', 'inventory_number', 'serial_number'],
                            data_value: str) -> int:
        params = {'object_type': object_type, 'data_typer': data_typer, 'data_value': data_value}
        pyuserside.validators.device.validate('get_device_id', **params)
        response = await self._api.request(self._cat, 'get_device_id', **params)
        return response.get('id')

    async def get_data(self, object_type: Literal['switch', 'onu', 'olt', 'radio', 'all'],
                       node_id: Optional[Union[str, int]] = None,
                       object_id: Optional[Union[str, int]] = None,
                       is_online: Optional[Union[str, int]] = None,
                       is_hide_ifaces_data: Optional[Union[str, int]] = None) -> List[DeviceData]:
        params = {'object_type': object_type,
                  'node_id': node_id,
                  'object_id': object_id,
                  'is_online': is_online,
                  'is_hide_ifaces_data': is_hide_ifaces_data}
        params = {k: v for k, v in params.items() if v is not None}
        pyuserside.validators.device.validate('get_data', **params)
        response = await self._api.request(self._cat, 'get_data', **params)
        response_class: Type[DeviceData] = DeviceData if is_hide_ifaces_data in [1, '1'] else DeviceDataWithIfaces
        return [response_class(**parameters) for parameters in response['data'].values()]


class Commutation(GenericUsersideCategory):
    def __init__(self, api: 'UsersideAPI'):
        super().__init__(category='commutation', api=api)

    async def get_data(self, object_type: Literal['customer', 'switch', 'radio', 'cross', 'fiber', 'splitter'],
                       object_id: Optional[Union[int, str]] = None,
                       is_finish_data: Optional[Union[int, str]] = None):
        params = {'object_type': object_type,
                  'object_id': object_id,
                  'is_finish_data': is_finish_data}
        params = {k: v for k, v in params.items() if v is not None}
        pyuserside.validators.commutation.validate('get_data', **params)
        response = await self._api.request(self._cat, 'get_data', **params)
        response = response['data']
        response_class = CommutationDataWithFinishData if is_finish_data in [1, '1'] else CommutationData
        return response_class(response)

    async def add(self, object_type: str = None,
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
        params = {k: v for k, v in params.items() if v is not None}
        pyuserside.validators.commutation.validate('add', **params)
        await self._api.request(self._cat, 'add', **params)

    async def delete(self, object_type: str, object_id: Union[str, int], object_port: Optional[Union[str, int]] = None):
        params = {'object_type': object_type,
                  'object_id': object_id,
                  'object_port': object_port,
                  }
        params = {k: v for k, v in params.items() if v is not None}
        pyuserside.validators.commutation.validate('delete', **params)
        await self._api.request(self._cat, 'delete', **params)


class Customer(GenericUsersideCategory):
    def __init__(self, api: 'UsersideAPI'):
        super().__init__('customer', api)

    async def get_abon_id(self, data_typer: str, data_value: str, is_skip_old: Optional[Union[int, str]] = None):
        params = {'data_typer': data_typer,
                  'data_value': data_value,
                  'is_skip_old': is_skip_old,
                  }
        params = {k: v for k, v in params.items() if v is not None}
        content = await self._api.request(self._cat, 'get_abon_id', **params)
        if content.get('Result') == 'OK':
            return content.get('Id')
        else:
            raise ValueError('Customer was not found')

    async def get_data(self, customer_id: Union[str, int]):
        params = {
            'customer_id': customer_id
        }
        content = await self._api.request(self._cat, 'get_data', **params)
        return CustomerData(**content['data'])


class Node(GenericUsersideCategory):
    def __init__(self, api: 'UsersideAPI'):
        super().__init__('node', api)

    async def get(self, address_id: Optional[Union[str, int]] = None, entrance_number: Optional[Union[str, int]] = None,
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
        params = {k: v for k, v in params.items() if v is not None}
        content = await self._api.request(self._cat, 'get', **params)
        return [NodeData(**parameters) for parameters in content['data'].values()]


class Task(GenericUsersideCategory):
    def __init__(self, api: 'UsersideAPI'):
        super().__init__('task', api)

    async def get_list(self,  author_employee_id: Optional[Union[str, int]] = None,
                       closer_employee_id: Optional[Union[str, int]] = None,
                       customer_id: Optional[Union[str, int]] = None, date_add_from: Optional[str] = None,
                       date_add_to: Optional[str] = None, date_change_from: Optional[str] = None,
                       date_change_to: Optional[str] = None, date_do_from: Optional[str] = None,
                       date_do_to: Optional[str] = None, date_finish_from: Optional[str] = None,
                       date_finish_to: Optional[str] = None, division_id: Optional[Union[str, int]] = None,
                       division_id_with_staff: Optional[Union[str, int]] = None,
                       employee_id: Optional[Union[str, int]] = None, house_id: Optional[Union[str, int]] = None,
                       is_expired: Optional[Union[str, int]] = None, node_id: Optional[Union[str, int]] = None,
                       state_id: Optional[Union[str, int]] = None, task_position: Optional[Union[str, int]] = None,
                       task_position_tadius: Optional[Union[str, int]] = None,
                       type_id: Optional[Union[str, int]] = None, watcher_employee_id: Optional[Union[str, int]] = None,
                       order_by: Optional[str] = None, limit: Optional[int] = None, offset: Optional[int] = None):
        params = {'author_employee_id':  author_employee_id,
                  'closer_employee_id': closer_employee_id,
                  'customer_id': customer_id,
                  'date_add_from': date_add_from,
                  'date_add_to': date_add_to,
                  'date_change_from': date_change_from,
                  'date_change_to': date_change_to,
                  'date_do_from': date_do_from,
                  'date_do_to': date_do_to,
                  'date_finish_from': date_finish_from,
                  'date_finish_to': date_finish_to,
                  'division_id': division_id,
                  'division_id_with_staff': division_id_with_staff,
                  'employee_id': employee_id,
                  'house_id': house_id,
                  'is_expired': is_expired,
                  'node_id': node_id,
                  'state_id': state_id,
                  'task_position': task_position,
                  'task_position_tadius': task_position_tadius,
                  'type_id': type_id,
                  'watcher_employee_id': watcher_employee_id,
                  'order_by': order_by,
                  'limit': limit,
                  'offset': offset,}
        params = {k: v for k, v in params.items() if v is not None}
        content = await self._api.request(self._cat, 'get_list', **params)
        return content['list'].split(',')

    async def show(self,
                   id: Union[str, int],
                   employee_id: Optional[Union[str, int]] = None,
                   is_without_comments: Optional[Union[str, int]] = None):
        """Show task information

        :type id: int
        :param id: task id

        :type employee_id: int
        :param employee_id: employee who will be shown in task view history

        :type is_without_comments: int
        :param is_without_comments: flag - return comments or not

        :return: `pyuserside.schema.task.TaskData`
        """
        params = {'id': id,
                  'employee_id': employee_id,
                  'is_without_comments': is_without_comments}
        params = {k: v for k, v in params.items() if v is not None}
        content = await self._api.request(self._cat, 'show', **params)
        pprint(content['data'])
        return TaskData(**content['data'])


class UsersideAPI:
    def __init__(self, url: str, key: str):
        self._url = url
        self._key = key
        self._session = None
        self.device = Device(self)
        self.commutation = Commutation(self)
        self.customer= Customer(self)
        self.node = Node(self)
        self.task = Task(self)

    def __getattr__(self, item):
        return GenericUsersideCategory(item, self)

    async def request(self, cat: str, action: str, **kwargs):
        close_after_request = False
        if not self._session:
            self._session = aiohttp.ClientSession()
            close_after_request = True
        params = {'key': self._key, 'cat': cat, 'action': action}
        params.update(kwargs)
        success = True
        async with self._session.get(url=self._url, params=params) as response:
            content = await response.text()
            if not response.ok:
                success = False
                error_message = content
            elif not response.content:
                success = False
                error_message = 'Empty response'
        if close_after_request:
            await self._session.close()
            self._session = None
        if success:
            return json.loads(content)
        raise ValueError(error_message)

    async def __aenter__(self):
        self._session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._session.close()
        self._session = None
