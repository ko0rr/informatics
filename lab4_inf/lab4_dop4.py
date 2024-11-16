from time import time

from lab4_main_dop3 import main03
from lab4_dop1 import main1
from lab4_dop2 import main2


def test():
    start03 = time()

    for i in range(100):
        main03('scheduleXML_thursday.xml', 'scheduleJSON_thursday.json')
    end03 = time() - start03

    start1 = time()
    for i in range(100):
        main1()
    end1 = time() - start1

    start2 = time()
    for i in range(100):
        main2('scheduleXML_thursday.xml', 'scheduleJSON_thursday.json')
    end2 = time() - start2

    print(f"Основное задание и доп3: {end03}")
    print(f"Доп1: {end1}")
    print(f"Доп2: {end2}")


test()
