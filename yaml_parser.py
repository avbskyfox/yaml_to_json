class TypeIsNotSerializable(Exception):
    pass


class Dumper:
    def __init__(self, indent):
        self.indent = indent
        self.__current_indent = 0

    def get_indent(self):
        if self.__current_indent == 0:
            return ''
        return ' ' * self.__current_indent

    def __add_indent(self):
        self.__current_indent += self.indent

    def __remove_indent(self):
        self.__current_indent -= self.indent

    @staticmethod
    def __key(val):
        return str(val)

    @staticmethod
    def __string(val):
        return f"\"{val}\""

    @staticmethod
    def __number(val):
        return str(val)

    def __scalar_array_item(self, val):
        return f'{self.get_indent()}- {self.deal_with_type(val)}\n'

    def __object_or_array_item(self, val):
        result = f'{self.get_indent()}-\n'
        self.__add_indent()
        result += f'{self.deal_with_type(val)}'
        self.__remove_indent()
        return result

    def __array_element(self, val):
        if type(val) in [list, dict]:
            return self.__object_or_array_item(val)
        if type(val) in [str, int, float]:
            return self.__scalar_array_item(val)

    def __array(self, val):
        if len(val) == 0:
            return f'{self.__current_indent}-\n'
        result_string = ''
        for item in val:
            result_string += self.__array_element(item)
        return result_string

    def __key_value_element(self, key, value):
        if type(value) in [str, int, float]:
            return f'{self.get_indent()}{key}: {self.deal_with_type(value)}\n'
        if type(value) in [list, dict]:
            result = f'{self.get_indent()}{key}:'
            self.__add_indent()
            result += f'\n{self.deal_with_type(value)}'
            self.__remove_indent()
            return result

    def __object(self, val: dict):
        result_string = ''
        for key, value in val.items():
            result_string += self.__key_value_element(key, value)
        return result_string

    def deal_with_type(self, val):
        if type(val) is list:
            return self.__array(val)
        if type(val) is dict:
            return self.__object(val)
        if type(val) in [float, int]:
            return self.__number(val)
        if type(val) is str:
            return self.__string(val)
        else:
            raise TypeIsNotSerializable(f"can not serialize value of type {type(val)}")


class YAML:
    @staticmethod
    def load_string(s: str):
        pass

    @staticmethod
    def dump_string(data, indent=2):
        return Dumper(indent=indent).deal_with_type(data)
