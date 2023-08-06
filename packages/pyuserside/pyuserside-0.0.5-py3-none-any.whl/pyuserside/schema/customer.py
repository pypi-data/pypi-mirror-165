from datetime import datetime
from dataclasses import dataclass
import ipaddress


@dataclass
class AdditionalData:
    id: int
    name: str
    value: str


@dataclass
class Agreement:
    number: str
    date: datetime | None


@dataclass
class TrafficPart:
    up: int
    down: int


@dataclass
class Traffic:
    month: TrafficPart


@dataclass
class Apartment:
    number: int


@dataclass
class Address:
    apartment: Apartment
    floor: str
    house_id: int
    type: str


class CustomerData:
    def __init__(self, **data):
        self.account_number = data.get('account_number')
        additional_fields = data.get('additional_customer_data')
        self.additional_customer_data = {}
        for additional_field in additional_fields.values():
            self.additional_customer_data[additional_field['id']] = additional_field['value']
        addresses = data.get('address')
        self.address = []
        for address in addresses:
            apartment = Apartment(address.get('apartment').get('number'))
            new_address = Address(apartment, address.get('floor'), address.get('house_id'), address.get('type'))
            self.address.append(new_address)
        agreements = data.get('agreement')
        self.agreement = []
        for agreement in agreements:
            if agreement.get('date'):
                new_agreement = Agreement(agreement.get('number'), datetime.strptime(agreement.get('date'), '%d.%m.%Y'))
            else:
                new_agreement = Agreement(agreement.get('number'), None)
            self.agreement.append(new_agreement)
        self.balance = data.get('balance')
        self.billing = data.get('billing')
        self.billing_id = data.get('billing_id')
        self.comment = data.get('comment')
        self.comment2 = data.get('comment2')
        self.credit = data.get('credit')
        self.date_activity = datetime.strptime(data.get('date_activity'), '%Y-%m-%d %H:%M:%S')
        self.date_activity_inet = datetime.strptime(data.get('date_activity_inet'), '%Y-%m-%d %H:%M:%S')
        self.date_connect = datetime.strptime(data.get('date_connect'), '%Y-%m-%d')
        self.date_create = datetime.strptime(data.get('date_create'), '%Y-%m-%d %H:%M:%S')
        self.date_positive_balance = datetime.strptime(data.get('date_positive_balance'), '%Y-%m-%d')
        self.email = data.get('email')
        self.flag_corporate = data.get('flag_corporate')
        self.full_name = data.get('full_name')
        self.id = data.get('id')
        ips_macs = data.get('ip_mac')
        self.ip_mac = {}
        for entry in ips_macs.values():
            self.ip_mac[ipaddress.ip_address(int(entry['ip']))] = entry['mac']
        self.is_disable = data.get('is_disable')
        self.is_in_billing = data.get('is_in_billing')
        self.login = data.get('login')
        self.mark = list(data.get('mark').keys()) if data.get('mark') else []
        self.phone = data.get('phone')
        self.state_id = data.get('state_id')
        self.tag = data.get('tag')
        self.tariff = data.get('tariff')
        traffic_info = data.get('traffic')
        traffic_part = TrafficPart(**traffic_info.get('month'))
        traffic = Traffic(traffic_part)
        self.traffic = traffic




