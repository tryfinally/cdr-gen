import sys
import csv
import random
import random_data
from collections import namedtuple
from typing import NamedTuple

class Subscriber(NamedTuple):
    msin  : str
    iemi  : str
    number: str


class MobileOperator:
    def __init__(self, record):
        self.mcc = record[0]
        self.mnc = record[2]
        self.iso = record[4]
        self.country = record[5]
        self.country_code = record[6]
        self.network = record[7]

    def generates_subscribers(self, n):
        msin = list(random_data.generate_set( lambda: random_data.msin() , n))
        iemi = list(random_data.generate_set( lambda: random_data.imei() , n))
        number = list(random_data.generate_set( lambda: random_data.subscriber_number(9) , n))
        self.subscribers = []
        for i in range(n):
            self.subscribers.append(Subscriber(msin[i], iemi[i], self.country_code + '0' + number[i]))

class MobileOperators:
    def __init__(self, file_name):
        self.operators = self.__load_operators(file_name)
        self.by_mcc = {}
        for row in self.operators:
            self.by_mcc.setdefault(row[0], []).append(MobileOperator(row))

    def get_operators_by_country(self, mcc):
        return self.by_mcc[mcc]

    def select_random_mcc(self, n):
        return random.sample(self.by_mcc.items(), n)

    def __load_operators(self,file_name):
        with open(file_name, mode='r') as infile:
            reader = csv.reader(infile)
            ops = list(reader)
            return ops[1:] # drop header first line

class Generator:
    def __init__(self, operators):
        self.mobile_operators = operators

    def test(self, n):
        mccs = self.mobile_operators.select_random_mcc(n)
        for mcc in mccs:
            for mo in mcc[1]:
                mo.generates_subscribers(n)
                print(mo.iso, mo.mcc, mo.mnc, mo.country_code, mo.subscribers)


def main():
    if len(sys.argv) < 3:
            print("Usage: ", sys.argv[0], "country_code subscribers")
            sys.exit(1)

    cc = sys.argv[1]
    nn = int(sys.argv[2])

    operators = MobileOperators('./mcc-mnc-table.csv')
    gen = Generator(operators)
    gen.test(nn)



if __name__ == "__main__":
    main()
