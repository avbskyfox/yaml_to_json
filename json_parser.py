from copy import deepcopy


class Dumber:
    def value(self, data):
        if type(data) is dict:
            return self.__object(data)
        elif type(data) is list:
            return self.__array(data)
        elif type(data) is str:
            return self.__string(data)
        elif type(data) is int or type(data) is float:
            return self.__numeric(data)

    def __object(self, data: dict):
        return '{' + self.__key_value_list(data) + '}'

    def __key_value_list(self, data: dict):
        if len(data) == 1:
            key = list(data)[0]
            return self.__key_value_element(key, data[key])
        else:
            fist_key = list(data)[0]
            fist_value = data[fist_key]
            data.pop(fist_key)
            return self.__key_value_element(fist_key, fist_value) + ', ' + self.__key_value_list(data)

    def __key_value_element(self, key, value):
        return self.__string(key) + ': ' + self.value(value)

    def __array(self, data: list):
        return '[' + self.__comma_separated_elements(data) + ']'
    
    def __comma_separated_elements(self, data: list):
        if len(data) == 1:
            return self.value(data[0])
        else:
            return self.value(data.pop(0)) + ', ' + self.__comma_separated_elements(data)

    @staticmethod
    def __string(data):
        return f'\"{data}\"'

    @staticmethod
    def __numeric(data):
        return str(data)


class JSON:
    @staticmethod
    def dump_string(data, dumper_class=Dumber):
        dumper = dumper_class()
        return dumper.value(deepcopy(data))
