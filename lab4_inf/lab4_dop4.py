from time import time

from lab4_main_dop3 import main03
from lab4_dop1 import main1
from lab4_dop2 import main2


def test():
    start_03 = time()

    for i in range(100):
        main03()
    end_03 = time() - start_03

    start_1 = time()
    for i in range(100):
        main1()
    end_1 = time() - start_1

    start_2 = time()
    for i in range(100):
        main2('scheduleXML_thursday.xml', 'scheduleJSON_thursday.json')
    end_2 = time() - start_2

    print(end_03, end_1, end_2)


test()