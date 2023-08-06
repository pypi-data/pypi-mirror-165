import abc
import json
from abc import ABC

import requests as requests

from ephemeralsrocket import ConnectionParams


class DbManagerProtocol(ABC):

    @abc.abstractmethod
    def fetch_database_info(self, name: str):
        pass

    @abc.abstractmethod
    def create_database(self, name: str):
        pass

    @abc.abstractmethod
    def create_date_time_properties_definition(self, db_name: str, object_name, definition: dict):
        pass

    @abc.abstractmethod
    def create_encrypt_definition(self, db_name: str, object_name, definition: dict):
        pass

    @abc.abstractmethod
    def create_search_definition(self, db_name: str, object_name, definition: dict):
        pass

    @abc.abstractmethod
    def exec_post(self, db_name, object_name, payload):
        pass

    @abc.abstractmethod
    def exec_get_one(self, db_name, object_name, _id):
        pass

    @abc.abstractmethod
    def exec_search(self, db_name, object_name, query_payload):
        pass

    @abc.abstractmethod
    def drop_database(self, name: str):
        pass


class DbManager(DbManagerProtocol):

    __cnn_params: ConnectionParams

    def __init__(self, connection_params: ConnectionParams):
        self.__cnn_params = connection_params

    def get_access_token(self):
        payload = {
            'name': self.__cnn_params.credentials.name,
            'secret': self.__cnn_params.credentials.secret,
            'grantType': self.__cnn_params.credentials.grant_type
        }
        token_response = requests.post(f'{self.__cnn_params.get_base_endpoint()}/accounts/token', json=payload)
        return json.loads(token_response.text)['access_token']

    def fetch_database_info(self, name: str):
        headers = {'Authorization': f'Bearer {self.get_access_token()}', 'Content-type': 'application/json'}
        url = f'{self.__cnn_params.get_base_endpoint()}/{name}'
        return requests.get(url, headers=headers)

    def create_database(self, name: str):
        headers = {'Authorization': f'Bearer {self.get_access_token()}', 'Content-type': 'application/json'}
        url = f'{self.__cnn_params.get_base_endpoint()}/{name}'
        return requests.post(url, data=json.dumps({
            'name': name,
            'description': f'Epemeral db for {name} app'
        }), headers=headers)

    def create_date_time_properties_definition(self, db_name: str, object_name, definition: dict):
        headers = {'Authorization': f'Bearer {self.get_access_token()}', 'Content-type': 'application/json'}
        url = f'{self.__cnn_params.get_base_endpoint()}/{db_name}/{object_name}/date-time-properties-definition'
        return requests.post(url, data=json.dumps(definition), headers=headers)

    def create_encrypt_definition(self, db_name: str, object_name, definition: dict):
        headers = {'Authorization': f'Bearer {self.get_access_token()}', 'Content-type': 'application/json'}
        url = f'{self.__cnn_params.get_base_endpoint()}/{db_name}/{object_name}/encrypt-definition'
        return requests.post(url, data=json.dumps(definition), headers=headers)

    def create_search_definition(self, db_name: str, object_name, definition: dict):
        headers = {'Authorization': f'Bearer {self.get_access_token()}', 'Content-type': 'application/json'}
        url = f'{self.__cnn_params.get_base_endpoint()}/{db_name}/{object_name}/search-definition'
        return requests.post(url, data=json.dumps(definition), headers=headers)

    def exec_get_one(self, db_name: str, object_name: str, _id: str):
        headers = {'Authorization': f'Bearer {self.get_access_token()}', 'Content-type': 'application/json'}
        url = f'{self.__cnn_params.get_base_endpoint()}/{db_name}/{object_name}/{_id}'
        return requests.get(url, headers=headers)

    def exec_post(self, db_name, object_name, payload):
        headers = {'Authorization': f'Bearer {self.get_access_token()}', 'Content-type': 'application/json'}
        url = f'{self.__cnn_params.get_base_endpoint()}/{db_name}/{object_name}'
        return requests.post(url, data=json.dumps(payload), headers=headers)

    def exec_search(self, db_name, object_name, query_payload):
        headers = {'Authorization': f'Bearer {self.get_access_token()}', 'Content-type': 'application/json'}
        url = f'{self.__cnn_params.get_base_endpoint()}/{db_name}/{object_name}/search'
        return requests.post(url, data=json.dumps(query_payload), headers=headers)

    def drop_database(self, name: str):
        headers = {'Authorization': f'Bearer {self.get_access_token()}', 'Content-type': 'application/json'}
        url = f'{self.__cnn_params.get_base_endpoint()}/{name}'
        return requests.delete(url, headers=headers)
