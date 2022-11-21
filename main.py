import json
import yaml

from yaml_parser import YAML
from json_parser import JSON


def main():
    with open('test_shcedule.yml') as f:
        string = f.read()

    # загрузкf сторонней библиотекой
    etalon_data = yaml.load(string, yaml.Loader)

    # загрузка кастомной библиотекой
    custom_data = YAML.load_string(string)

    # проверяем, что полученные объекты идентичны
    if custom_data == etalon_data:
        print(custom_data)

    # сериализуем стандартным JSON
    etalon_string = json.dumps(custom_data, ensure_ascii=False)

    # сериализуем кастомным JSON
    custom_string = JSON.dump_string(custom_data)

    # проверяем идентичность результатов
    if etalon_string == custom_string:
        print(custom_string)

    # сохраняем в файл
    with open('shcedule.json', 'w') as f:
        f.write(custom_string)


if __name__ == '__main__':
    main()
