import yaml
from yaml.loader import SafeLoader

from yaml_parser import YAML
from json_parser import JSON
import re


# без re.DOTALL мы сломаемся на первом же переносе строки
number_regex = re.compile(r"(-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?)\s*(.*)", re.DOTALL)

def parse_number(src):
    match = number_regex.match(src)
    print(match)
    if match is not None:
        number, src = match.groups()
        return eval(number), src  # использовать eval - не лучшее решение, но самое простое


from yaml import dump

data = {
    'tuesday':
        [
            {
                'time': '10:00',
                'address': 'St.Ptersburg',
                'class': 123,
                'discipline': 'Mathematica'
            },
            {
                'time': '12:00',
                'address': 'St.Ptersburg',
                'class': 4523,
                'discipline': 'Biology'
            },
            {
                'time': '14:00',
                'address': 'St.Ptersburg',
                'class': 32,
                'discipline': 'Programming'
            }
        ]
}


def main():
    with open('schedule.yaml') as f:
        s = f.read()
    print(yaml.load(s, Loader=SafeLoader))



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
