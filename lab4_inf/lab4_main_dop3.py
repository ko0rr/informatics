"""     Вариант 1: XML -> JSON 
        Дни: понедельник и четверг  """


def remove_duplicate(data):
    """ функция проверяет, существует ли текущий ключ
        finally - count = element:  количество раз, к-е он встречается в data
        если ключа нет - добавляем его """

    count = {}
    for element in data:
        if element in count.keys():
            count[element] += 1
        else:
            count[element] = 1
    data.clear()
    for key in count.keys():        # оставляем только уникальные ключи
        data.append(key)


def validate_xml_lines(array):
        """ Функция проверяет, соответствует ли входной файл формату XML """
    opened_tags = []     # Стек для отслеживания открытых тегов

    for i, line in enumerate(array):
        stripped_line = line.strip()    # Убираем лишние пробелы

        # Разбиваем строку на теги
        while "<" in stripped_line:
            start_index = stripped_line.find("<")
            end_index = stripped_line.find(">", start_index)

            if end_index == -1:    # -1 когда не найден элемент
                print(f"Ошибка: Незакрытый тег: {line.strip()}")
                return False

            tag = stripped_line[start_index + 1:end_index].strip()
            stripped_line = stripped_line[end_index + 1:]  # Оставляем остаток строки

            # Определяем тип тега
            if tag.startswith("?") or tag.startswith("!"):  # Пропускаем служебные теги
                continue
            elif tag.startswith("/"):  # Закрывающий тег
                tag_name = tag[1:]
                if not opened_tags or opened_tags[-1] != tag_name:
                    print(
                        f"ошибка: тег в строке {i + 1}: </{tag_name}> не соответствует <{opened_tags[-1] if opened_tags else 'нет открытого тега'}>")
                    return False
                opened_tags.pop()
            elif tag.endswith("/"):  # Самозакрывающийся тег
                continue
            else:  # Открывающий тег
                tag_name = tag.split()[0]
                opened_tags.append(tag_name)

    # Проверяем незакрытые теги
    if opened_tags:
        print(f"ошибка: незакрытые теги: {opened_tags}")
        return False
    else:
        print("всё оке")
        return True


def main03(xml_f, json_f):
    stack = []  # вложенные теги
    lines = []  # строки json
    to_be_listed = []
    """ если текущий тег уже встречался -> to_be_listed
        для обработки вложенности """
    #array = xml_f.readlines()
    s = '' # последний тег

    with open(xml_f, "r", encoding="utf-8") as xml:
        array = xml.readlines()
        lines.append('{\n')     # открывает блок кода в json
        for line in array:
            if not validate_xml_lines(array):
                print('некорректный xml')
                return
            if line.strip() == '<?xml version="1.0" encoding="UTF-8" ?>':   # пропускаем первую строку тк она не конверируется в json
                continue
            tag = line[line.find('<') + 1:line.find('>')]  # выделяем тег(срез строки)

            if s == tag: # является ли tag вложенным относительно s
                to_be_listed.append(tag) # вложен

            if '/' not in tag and tag not in stack:
                stack.append(tag)
                if not (f'<{tag}>' in line and f'</{tag}>' in line):
                    lines.append('\t' * len(stack) + f'"{tag}": ' + '{' + '\n')   # если тег не является закрывающим, то создаётся вложенный объект

            if f'<{tag}>' in line and f'</{tag}>' in line:
                value = line[line.find('>') + 1: line.rfind('<')]
                lines.append('\t' * len(stack) + f'"{tag}": ' + f'"{value}",' + '\n') # если тег закрывающий или самозакрывающийся - его значение добавляетсякак значение для ключа
                s = stack.pop() # нашли закрывающий тег для текущего тега - очищаем, чтобы добавить новый текущий объект

            if '/' in tag and tag[1:] in stack:
                lines.append('\t' * len(stack) + '},\n') # для закрывающего тега добавляется строка с закрывающей скобкой для завершения блока кода
                s = stack.pop()

        lines.append('}')

    remove_duplicate(to_be_listed) # удаление дубликатов во вложенных тегах

    for i in range(len(lines) - 1): # форматирование закрывающими скобками - обрезаются, если на предыдущей есть закрывающая скобка
        if lines[i + 1].strip() in ['},', '}']:
            lines[i] = lines[i].rstrip()[:-1] + '\n'

    for sp in to_be_listed:
        first = True
        tab_start = 0
        for i in range(len(lines)):
            tab = lines[i].count('\t')
            if sp in lines[i] and first:
                tab_start = tab
                lines[i] = lines[i].replace('{', '[\n' + ('\t' * (tab + 1)) + '{') # если тег вложен - преобразовывается квадратными скобками и отступами
                first = False                                                      # расстановка открывающих скобок
            elif sp in lines[i]:
                lines[i] = lines[i].replace(f'"{sp}": ', '')

            if tab < tab_start:
                lines[i - 1] = lines[i - 1] + ('\t' * (tab + 1)) + ']\n'
                break

        tab = False
        for i in range(len(lines)):
            if f'"{sp}"' in lines[i]:
                tab = True
                continue
            if tab:
                lines[i] = '\t' + lines[i]
            if ']' in lines[i] and lines[i][lines[i].find('}'):].count('\t') == tab_start:    # расстановка закрыающих строк
                break

    with open(json_f, "w", encoding="utf-8") as json:
        for i in lines:
            json.write(i)
        #print('converted into scheduleJSON_thursday.json file')



main03('scheduleXML_thursday.xml', 'scheduleJSON_thursday.json') #основное задание
main03('scheduleXML_monday.xml', 'schedule1JSON_monday.json')   #доп3
main03('scheduleXML_thursday.xml', 'schedule2JSON_thursday.json')   #доп3
