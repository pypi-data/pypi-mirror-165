from dataclasses import dataclass


@dataclass
class OneConnection:
    object_type: str
    object_id: int
    direction: int
    interface: int
    comment: str
    connect_id: int


class CommutationData:
    def __init__(self, commutation_table: dict):
        self.commutation = {}
        for local_interface, connections in commutation_table.items():
            self.commutation[local_interface] = {}
            for index, connection in enumerate(connections):
                self.commutation[local_interface][index] = OneConnection(**connection)

    def __repr__(self):
        return f'CommutationData({len(self.commutation.keys())} connections)'


class CommutationDataWithFinishData:
    def __init__(self, commutation_table: dict):
        self.commutation = {}
        for local_interface, connections in commutation_table.items():
            self.commutation[local_interface] = {}
            for index, connection in connections.items():
                self.commutation[local_interface][index] = OneConnection(**connection)

    def __repr__(self):
        return f'CommutationData({len(self.commutation.keys())} connections)'
