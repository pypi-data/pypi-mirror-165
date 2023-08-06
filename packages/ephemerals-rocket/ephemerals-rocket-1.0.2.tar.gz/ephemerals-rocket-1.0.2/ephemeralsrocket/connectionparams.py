from ephemeralsrocket import Credentials


class ConnectionParams:

    protocol: str
    host_name: str
    port_number: int
    credentials: Credentials

    def __init__(self, protocol: str, host_name: str, port_number: int, credentials: Credentials):
        self.protocol = protocol
        self.host_name = host_name
        self.port_number = port_number
        self.credentials = credentials

    def get_base_endpoint(self):
        return f'{self.protocol}://{self.host_name}:{self.port_number}'
