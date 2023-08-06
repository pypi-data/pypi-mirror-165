import json
from typing import Dict
from properties import Properties

class ConfigFileHelper:

    def _set_value_in_json(self, json_object, key, value):
        index = key.find('.')
        if index < 0:
            if isinstance(value, bool):
                json_object[key] = bool(value)
            elif value.isnumeric():
                json_object[key] = int(value)
            else:
                json_object[key] = value
        else:
            base_key = key[0:index]
            new_key = key[index + 1:len(key)]
            self.__set_value_in_json(json_object[base_key], new_key, value)

    def _set_values_in_json_file(self, json_config_file_path:str, value_mapping:Dict, output_file_path:str = None):
        file = open(json_config_file_path, 'r')
        json_object = json.load(file)
        file.close()

        for key in value_mapping:
            self._set_value_in_json(json_object, key, value_mapping[key])

        return json_object
        

    def set_values_in_json_file(self, json_config_file_path:str, value_mapping:Dict, output_file_path:str = None) -> json:
        json_object:json = self._set_values_in_json_file(json_config_file_path, value_mapping)
        if output_file_path != None:
            file = open(output_file_path, 'w')
            json.dump(json_object, file)
            file.close()
            return None
        return json_object

    def set_values_in_properties_file(self, properties_config_file_path:str, value_mapping:Dict, output_file_path:str = None) -> Properties:
        properties:Properties = Properties()

        properties.load(properties_config_file_path)
        
        for key in value_mapping:
            properties.put(key, value_mapping[key])
        
        if output_file_path != None:
            properties.dump(output_file_path)
            return None
            
        return properties
        