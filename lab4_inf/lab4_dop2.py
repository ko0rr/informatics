import re
def remove_duplicate(data):

    """функция проверяет, существует ли текущий ключ
    count = element:  """
    count = {}
    for element in data:
        if element in count.keys():
            count[element] += 1
        else:
            count[element] = 1
    data.clear()
    for key in count.keys():
        data.append(key)


def main2(xml_f, json_f):
    stack = []
    lines = []
    to_be_listed = []
    s = ''

    with open(xml_f, "r", encoding="utf-8") as xml:
        lines.append('{\n')
        for line in xml.readlines():
            close = False
            if line.strip() == '<?xml version="1.0" encoding="UTF-8" ?>':
                continue
            tag = re.findall('<(.*?)>', line)                                           # regex
            if len(tag) == 2:
                tag, close_tag = tag
                close = True
            else:
                tag = tag[0]
            if s == tag:
                to_be_listed.append(tag)

            if '/' not in tag and tag not in stack:
                stack.append(tag)
                if not (f'<{tag}>' in line and f'</{tag}>' in line):
                    lines.append('\t' * len(stack) + f'"{tag}": ' + '{' + '\n')

            if close:
                value = re.findall('>(.*)<', line)[0]                                   # regex
                lines.append('\t' * len(stack) + f'"{tag}": ' + f'"{value}",' + '\n')
                s = stack.pop()

            if '/' in tag and tag[1:] in stack:
                lines.append('\t' * len(stack) + '},\n')
                s = stack.pop()

        lines.append('}')

    remove_duplicate(to_be_listed)

    for i in range(len(lines) - 1):
        if lines[i + 1].strip() in ['},', '}']:
            lines[i] = lines[i].rstrip()[:-1] + '\n'

    for sp in to_be_listed:
        first = True
        start = 0
        for i in range(len(lines)):
            tabs = lines[i].count('\t')
            if sp in lines[i] and first:
                start = tabs
                lines[i] = lines[i].replace('{', '[\n' + ('\t' * (tabs + 1)) + '{')
                first = False
            elif sp in lines[i] and not first:
                lines[i] = lines[i].replace(f'"{sp}": ', '')

            if tabs < start:
                lines[i - 1] = lines[i - 1] + ('\t' * (tabs + 1)) + ']\n'
                break

        tab = False
        for i in range(len(lines)):
            if f'"{sp}"' in lines[i]:
                tab = True
                continue
            if tab:
                lines[i] = '\t' + lines[i]
            if ']' in lines[i] and lines[i][lines[i].find('}'):].count('\t') == start:
                break

    with open(json_f, "w", encoding="utf-8") as json:
        for i in lines:
            json.write(i)
        print('converted')


main2('scheduleXML_thursday.xml', 'dop2JSON.json')
