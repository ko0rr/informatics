import xmltodict
import json


def main1():
    with open('scheduleXML_thursday.xml', 'r', encoding='UTF-8') as x:
        x = x.read()
        d = xmltodict.parse(x, encoding='utf-8')

        json_obj = json.dumps(d, indent=4, ensure_ascii=False)
    with open('dop1JSON.json', 'w', encoding='UTF-8') as s:
        s.write(json_obj)
        print('converted into dop1JSON.json file')


main1()