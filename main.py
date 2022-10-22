from yaml_parser import YAML
from json_parser import JSON
from yaml import dump

# data = {
#     'tuesday':
#         [
#             {
#                 'time': '10:00',
#                 'address': 'St.Ptersburg',
#                 'class': 123,
#                 'discipline': 'Mathematica'
#             },
#             {
#                 'time': '12:00',
#                 'address': 'St.Ptersburg',
#                 'class': 4523,
#                 'discipline': 'Biology'
#             },
#             {
#                 'time': '14:00',
#                 'address': 'St.Ptersburg',
#                 'class': 32,
#                 'discipline': 'Programming'
#             }
#         ]
# }


def main():
    with open('schedule.yaml') as f:
        s = f.read()
    data = YAML.load_string(s)
    s = JSON.dump_string(data)
    print(s)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
