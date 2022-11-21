class TypeIsNotSerializable(Exception):
    pass


class BadSyntax(Exception):
    pass


class Dumper:
    def __init__(self, indent):
        self.indent = indent
        self.__current_indent_count = 0

    def __current_indent(self):
        if self.__current_indent_count == 0:
            return ''
        return ' ' * self.__current_indent_count

    def __add_indent(self):
        self.__current_indent_count += self.indent

    def __remove_indent(self):
        self.__current_indent_count -= self.indent

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
        return f'{self.__current_indent()}- {self.process(val)}\n'

    def __object_or_array_item(self, val):
        result = f'{self.__current_indent()}-\n'
        self.__add_indent()
        result += f'{self.process(val)}'
        self.__remove_indent()
        return result

    def __array_element(self, val):
        if type(val) in [list, dict]:
            return self.__object_or_array_item(val)
        if type(val) in [str, int, float]:
            return self.__scalar_array_item(val)

    def __array(self, val):
        if len(val) == 0:
            return f'{self.__current_indent_count}-\n'
        result_string = ''
        for item in val:
            result_string += self.__array_element(item)
        return result_string

    def __key_value_element(self, key, value):
        if type(value) in [str, int, float]:
            return f'{self.__current_indent()}{key}: {self.process(value)}\n'
        if type(value) in [list, dict]:
            result = f'{self.__current_indent()}{key}:'
            self.__add_indent()
            result += f'\n{self.process(value)}'
            self.__remove_indent()
            return result

    def __object(self, val: dict):
        result_string = ''
        for key, value in val.items():
            result_string += self.__key_value_element(key, value)
        return result_string

    def process(self, val):
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


class Loader:
    def __init__(self, indent):
        self.__indent = indent
        self.__current_indent_count = 0

    def __remove_indent(self, string: str):
        result = ''
        for row in string.split('\n'):
            result += f'{row.removeprefix(" " * self.__indent)}\n'
        return result[0:-1]

    @staticmethod
    def __string(string: str):
        return string[1: -1]

    @staticmethod
    def __number(string: str):
        if string.find('.') > 0:
            return float(string)
        else:
            return int(string)

    def __key(self, string: str):
        return self.__scalar_item(string)

    def __key_value_element(self, string: str):
        key = string[0:string.find(':')]
        prevalue = string[string.find(':')+2:]
        if prevalue.startswith('  ' * self.__indent):
            value = self.__remove_indent(prevalue)
        else:
            value = prevalue
        if self.__type(value) == 'object':
            return key, self.process(value)
        if self.__type(value) == 'scalar':
            return key, self.process(value)

    def __key_value_list(self, string: str):
        result = []
        rows = string.split('\n')
        buffer = str()
        for i in range(0, len(rows)):
            if rows[i] == '':
                continue
            buffer += f'{rows[i]}\n'
            try:
                if not (rows[i+1].startswith(' ' * self.__indent) or rows[i+1].startswith('-')):
                    result.append(buffer[0:-1])
                    buffer = str()
            except IndexError:
                result.append(buffer[0:-1])
        return result

    def __array_element(self, string: str):
        if string.startswith('- '):
            return self.__scalar_item(string.removeprefix('- ').strip('\n '))
        if string.startswith('-\n'):
            return self.__object_or_array_item(self.__remove_indent(string.removeprefix('-\n')))

    def __array_element_list(self, string: str):
        result = []
        rows = string.split('\n')
        buffer = str()
        for i in range(0, len(rows)):
            # if i == 1: # хз, зачем вообще это было нужно
            #     continue
            if rows[i].startswith('- '):
                result.append(rows[i][2:])
            buffer += f'{rows[i]}\n'
            try:
                if rows[i+1].startswith('-'):
                    result.append(buffer[0:-1])
                    buffer = str()
            except IndexError:
                result.append(buffer)
        return result

    def __array(self, string: str):
        result = []
        for element in self.__array_element_list(string):
            result.append(self.__array_element(element))
        return result

    def __object(self, string: str):
        result = {}
        for key_value in self.__key_value_list(string):
            key, value = self.__key_value_element(key_value)
            result.update({key: value})
        return result

    def __scalar_item(self, string: str):
        def is_float(string: str):
            if string.find('.') > 0 and len(string.split('.')) == 2:
                return True
        if is_float(string) or string.isnumeric():
            return self.__number(string)
        else:
            return self.__string(string)

    def __object_or_array_item(self, string: str):
        rows = string.split('\n')
        if rows[0].startswith('- ') or rows[0] == '-':
            return self.__array(string)
        elif rows[0].find(':\n') > 0 or rows[0].find(': ') > 0:
            return self.__object(string)
        else:
            raise BadSyntax

    @staticmethod
    def __type(string: str):
        if len(string.split('\n')) > 1:
            return 'object'
        else:
            return 'scalar'

    def process(self, string: str):
        if self.__type(string) == 'object':
            return self.__object_or_array_item(string)
        if self.__type(string) == 'scalar':
            return self.__scalar_item(string)


class YAML:
    @staticmethod
    def load_string(s: str, indent=4, loader_class=Loader):
        return loader_class(indent=indent).process(s)

    @staticmethod
    def dump_string(data, indent=4, dumper_class=Dumper):
        return dumper_class(indent=indent).process(data)
