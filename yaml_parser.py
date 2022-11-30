import re


class TypeIsNotSerializable(Exception):
    pass


class BadSyntax(Exception):
    pass


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

    @staticmethod
    def __re_type(string: str):
        if re.search(r'.*: ', string) or re.search(r'.*\n', string):
            return 'object'
        if re.match(r'-\n', string) or re.match(r'- ', string):
            return 'array'
        else:
            return 'scalar'

    def process(self, string: str):
        if self.__type(string) == 'object':
            return self.__object_or_array_item(string)
        if self.__type(string) == 'scalar':
            return self.__scalar_item(string)

    def re_process(self, string: str):
        if self.__re_type(string) == 'object':
            return self.__object(string)
        elif self.__re_type(string) == 'array':
            return self.__array(string)
        elif self.__re_type(string) == 'scalar':
            return self.__scalar_item(string)


class YAML:
    @staticmethod
    def load_string(s: str, indent=4, loader_class=Loader):
        return loader_class(indent=indent).process(s)

    @staticmethod
    def re_load_string(s: str, indent=4, loader_class=Loader):
        return loader_class(indent=indent).re_process(s)
