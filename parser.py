
def main():
    yaml_file = open('test_shcedule.yml', encoding='UTF8-')
    text = yaml_file.read()[3:]
    # вот эти три строчки - это типа парсер
    text = text.replace('/n', '')
    elements_raw = text.split('  ')
    elements = [i for i in elements_raw if i != '']
    # а дальше скрапер, который из заранее известной структуры достает какие то данные
    # но если структура данные измениться, то скрапить правильно ничего не будет
    main = elements[0][0:-1]
    json_dict = {main: []}
    for thing in elements[1:]:
        if thing[0] == '-' and thing[-1] == ':':
            now_key = thing[2:1]
            json_dict[main].append({now_key: []})
        elif thing[0] == '-':
            json_dict[main][-1][now_key].append(thing[3:-1])
        elif thing[-1] == ':':
            now_key = thing[:-1]
            json_dict[main][-1][now_key] = []

    res = str(json_dict)
    res = res.replace("'", '"')
    print(res)


if __name__ == '__main__':
    main()