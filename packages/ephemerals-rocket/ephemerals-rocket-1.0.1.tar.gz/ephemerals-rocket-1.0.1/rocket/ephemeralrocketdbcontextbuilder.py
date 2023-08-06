from typing import List

from rocket import EphemeralRocketDbContext, DbManagerProtocol


class EphemeralRocketDbContextBuilder:

    __date_time_properties_definitions: dict
    __encrypt_definitions: dict
    __search_definitions: dict
    __items: dict

    def __init__(self):
        self.__date_time_properties_definitions = {}
        self.__encrypt_definitions = {}
        self.__search_definitions = {}
        self.__items = {}

    def add_date_properties_definitions(self, object_name, definition: dict):
        if object_name not in self.__date_time_properties_definitions:
            self.__date_time_properties_definitions[object_name] = {}
        self.__date_time_properties_definitions[object_name] = definition
        return self

    def add_encrypt_definitions(self, object_name, definition: dict):
        if object_name not in self.__encrypt_definitions:
            self.__encrypt_definitions[object_name] = {}
        self.__encrypt_definitions[object_name] = definition
        return self

    def add_search_definitions(self, object_name, definition: dict):
        if object_name not in self.__search_definitions:
            self.__search_definitions[object_name] = {}
        self.__search_definitions[object_name] = definition
        return self

    def add_items(self, object_name, items: List[dict]):
        if object_name not in self.__items:
            self.__items[object_name] = []
        self.__items[object_name].extend(items)
        return self

    def build(self, db_context: dict,
              db_manager: DbManagerProtocol = None):
        return EphemeralRocketDbContext(db_context,
                                        self.__date_time_properties_definitions,
                                        self.__encrypt_definitions,
                                        self.__search_definitions,
                                        self.__items,
                                        db_manager)
