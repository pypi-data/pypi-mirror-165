
from enum import Enum
from re import S

class _PropAttr(Enum):
    key = 'key'
    value = 'value'

class Properties:

    _props = []

    def __init__(self, equals_character:str = '='):
        self.equals_character = equals_character

    def _is_a_valid_line(self, line:str) -> bool:
        return line and not line.strip().startswith('#')

    def _get_equals_character_index(self, line:str) -> int:
        try:
            index:int = line.index(self.equals_character)
            return index
        except:
            return None

    def _parse_property_value(self, original_value:str) -> str:
        value:str = original_value.strip()
        if value.startswith('"') and value.endswith('"'):
            value = value[1:len(value) - 1]
        return value

    def _create_property(self, key:str, value:str):
        return {
            _PropAttr.key.value:  key, 
            _PropAttr.value.value: value
        }

    def _add_line_to_properties(self, line:str):
        if self._is_a_valid_line(line):
            index:int = line.index(self.equals_character)
            value:str = None
            if index:
                value = self._parse_property_value(line[index+1:len(line)])
            else:
                index = len(line)
            key:str = line[0:index].strip()
            prop = self._create_property(key, value)
            self._props.append(prop)

    def load(self, properties_file_path:str):
        with open(properties_file_path, 'r') as file:
            line:str = 'INIT'
            while line:
                line = file.readline()
                if line:
                    self._add_line_to_properties(line)

    def get(self, key:str) -> str:
        result_item = list(filter(lambda item : item[_PropAttr.key.value] == key, self._props))
        return result_item[0][_PropAttr.value.value] if len(result_item) > 0 else None

    def put(self, key:str, value:str):
        item_found = self.get(key)
        if item_found == None:
            self._props.append(self._create_property(key, value))
        else:
            _tmp_props = []
            for prop in self._props:
                if prop[_PropAttr.key.value] == key:
                    _tmp_props.append(self._create_property(key, value))
                else:
                    _tmp_props.append(prop)
            self._props = _tmp_props

    def _prop_to_string(self, prop):
        if prop == None:
            return ''
        return prop[_PropAttr.key.value] + '=' + (prop[_PropAttr.value.value] if prop[_PropAttr.key.value] != None else '')

    def dump(self, output_file_path:str):
        with open(output_file_path, 'w') as file:
            for prop in self._props:
                file.write(self._prop_to_string(prop))

    def _prop_to_string(self, prop) -> str:
        if prop == None:
            return ''
        prop_str:str = '[{key}={value}]'.format(key = prop[_PropAttr.key.value], value = prop[_PropAttr.value.value])
        return prop_str

    def to_string(self) -> str:
        if self._props and len(self._props) > 0:
            str_props:str='{'
            for prop in self._props:
                str_props += self._prop_to_string(prop) + ','
            return str_props[0:len(str_props) - 1] + '}'
        else:
            return '\{\}'