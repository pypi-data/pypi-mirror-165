from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Any


@dataclass
class AdditionalData:
    id: int
    caption: str
    value: str


@dataclass
class Address:
    addressId: int
    apartament: str
    text: str


@dataclass
class Attach:
    id: int
    dateAdd: datetime
    fileName: str
    fileSystemPath: str


@dataclass
class Comment:
    id: int
    employee_id: int
    dateAdd: datetime
    comment: str
    attach: Optional[List[Attach]]


@dataclass
class Customer:
    id: int
    fullName: str
    login: Optional[str] = None
    dateActivity: Optional[str] = None

@dataclass
class TaskDate:
    complete: Any
    create: datetime
    deadline_individual_hour: int
    runtime_individual_hour: int
    todo: Optional[datetime]
    update: Optional[datetime]


@dataclass
class TaskStaff:
    division: List[int]
    employee: List[int]


@dataclass
class TaskState:
    id: int
    name: str
    systemRole: int


@dataclass
class TaskType:
    id: int
    name: str


class TaskData:
    def __init__(self, **data):
        additional_data = data.get('additional_data')
        self.additional_data = [AdditionalData(**ad_data) for ad_data in additional_data.values()] if additional_data else []
        self.address = Address(**data.get('address'))
        self.author_employee_id = data.get('author_employee_id')
        self.comments = []
        comments = data.get('comments')
        for comment in comments.values():
            attaches = comment.get('attach')
            comment_data = comment.copy()
            if attaches:
                attaches = [Attach(**attach) for attach in attaches.values()]
                comment_data.pop('attach')
            self.comments.append(Comment(**comment_data, attach=attaches))
        self.customer = Customer(**data.get('customer'))
        self.date = TaskDate(**data.get('date'))
        self.description = data.get('description')
        self.description_short = data.get('description_short')
        self.id = data.get('id')
        self.node = data.get('node')
        self.parentTaskId = data.get('parentTaskId')
        self.priceCustom = data.get('priceCustom')
        self.priority = data.get('priority')
        staff = data.get('staff')
        staff_division = staff.get('division')
        staff_employee = staff.get('employee')
        staff_division = list(staff_division.values()) if staff_division else []
        staff_employee = list(staff_employee.values()) if staff_employee else []
        self.staff = TaskStaff(division=staff_division, employee=staff_employee)
        self.state = TaskState(**data.get('state'))
        self.type = TaskType(**data.get('type'))
        self.volumeCustom = data.get('volumeCustom')
        self.watcher_employee_list = data.get('watcher_employee_list')
