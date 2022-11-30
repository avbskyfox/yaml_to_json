import json
import yaml
import time

from yaml_parser import YAML
from json_parser import JSON


def time_test(func):
    start_time = time.time()
    func()
    return time.time() - start_time


def case1():
    with open('test_shcedule.yml') as f:
        result_string = f.read()

    data = YAML.load_string(result_string)
    result_string = JSON.dump_string(data)

    return result_string
    # with open('shcedule1.json', 'w') as f:
    #     f.write(result_string)


def case2():
    with open('test_shcedule.yml') as f:
        string = f.read()

    data = yaml.load(string, Loader=yaml.Loader)
    result_string = json.dumps(data, ensure_ascii=False)

    return result_string
    # with open('shcedule2.json', 'w') as f:
    #     f.write(result_string)


def case3():
    with open('test_shcedule.yml') as f:
        result_string = f.read()

    data = YAML.re_load_string(result_string)
    result_string = JSON.dump_string(data)

    return result_string

    # with open('shcedule_re.json', 'w') as f:
    #     f.write(result_string)


def case4():
    print(f'Case1 time: {time_test(case1)}')
    print(f'Case2 time: {time_test(case2)}')
    print(f'Case3 time: {time_test(case3)}')



if __name__ == '__main__':
    print('Case 1:')
    print(case1())
    print('\nCase 2:')
    print(case2())
    print('\nCase 3:')
    print(case3())
    print('\nCase 4:')
    case4()

