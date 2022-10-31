from yaml_parser import YAML
from json_parser import JSON


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
    print(YAML.dump_string(data, 2))


if __name__ == '__main__':
    main()
