import abc
import json
from abc import ABC

import requests as requests


class DbManagerProtocol(ABC):
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
    def exec_search(self, db_name, object_name, query_payload):
        pass

    @abc.abstractmethod
    def drop_database(self, name: str):
        pass


class DbManager(DbManagerProtocol):

    __db_context: dict

    def __init__(self, db_context):
        self.__db_context = db_context

    def get_access_token(self):
        if self.__db_context.get('account').get('grantType') == 'service':
            payload = {
                'name': self.__db_context.get('account').get('name'),
                'secret': self.__db_context.get('account').get('secret'),
                'grantType': self.__db_context.get('account').get('grantType')
            }
        else:
            payload = {
                'secret': self.__db_context.get('account').get('secret'),
                'grantType': self.__db_context.get('account').get('grantType')
            }
        r = requests.post(f'{self.__db_context.get("baseEndpoint")}/accounts/token', json=payload)
        return json.loads(r.text)['access_token']

    def create_database(self, name: str):
        headers = {'Authorization': f'Bearer {self.get_access_token()}', 'Content-type': 'application/json'}
        url = f'{self.__db_context.get("baseEndpoint")}/{name}'
        return requests.post(url, data=json.dumps({
            'name': name,
            'description': f'Epemeral db for {name} app'
        }), headers=headers)

    def create_date_time_properties_definition(self, db_name: str, object_name, definition: dict):
        headers = {'Authorization': f'Bearer {self.get_access_token()}', 'Content-type': 'application/json'}
        url = f'{self.__db_context.get("baseEndpoint")}/{db_name}/{object_name}/date-time-properties-definition'
        return requests.post(url, data=json.dumps(definition), headers=headers)

    def create_encrypt_definition(self, db_name: str, object_name, definition: dict):
        headers = {'Authorization': f'Bearer {self.get_access_token()}', 'Content-type': 'application/json'}
        url = f'{self.__db_context.get("baseEndpoint")}/{db_name}/{object_name}/encrypt-definition'
        return requests.post(url, data=json.dumps(definition), headers=headers)

    def create_search_definition(self, db_name: str, object_name, definition: dict):
        headers = {'Authorization': f'Bearer {self.get_access_token()}', 'Content-type': 'application/json'}
        url = f'{self.__db_context.get("baseEndpoint")}/{db_name}/{object_name}/search-definition'
        r = requests.post(url, data=json.dumps(definition), headers=headers)
        return r

    def exec_post(self, db_name, object_name, payload):
        headers = {'Authorization': f'Bearer {self.get_access_token()}', 'Content-type': 'application/json'}
        url = f'{self.__db_context.get("baseEndpoint")}/{db_name}/{object_name}'
        return requests.post(url, data=json.dumps(payload), headers=headers)

    def exec_search(self, db_name, object_name, query_payload):
        headers = {'Authorization': f'Bearer {self.get_access_token()}', 'Content-type': 'application/json'}
        url = f'{self.__db_context.get("baseEndpoint")}/{db_name}/{object_name}/search'
        return requests.post(url, data=json.dumps(query_payload), headers=headers)

    def drop_database(self, name: str):
        headers = {'Authorization': f'Bearer {self.get_access_token()}', 'Content-type': 'application/json'}
        url = f'{self.__db_context.get("baseEndpoint")}/{name}'
        return requests.delete(url, headers=headers)
