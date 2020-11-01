import sys
import csv
import random
import datetime
import random_data
from collections import namedtuple
from typing import NamedTuple

class Subscriber(NamedTuple):
    msin  : str
    imei  : str
    imsi  : str
    msisdn: str


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
        imei = list(random_data.generate_set( lambda: random_data.imei() , n))
        number = list(random_data.generate_set( lambda: random_data.subscriber_number(9) , n))
        self.subscribers = []
        for i in range(n):
            imsi = self.mcc + self.mnc + msin[i]
            msisdn = self.country_code + '0' + number[i]
            self.subscribers.append(Subscriber(msin[i], imei[i], imsi, msisdn))

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

    def generate_cdrs(self, operators_n, subscribers_n, cdr_n):
        self.gen_operators_population(operators_n, subscribers_n)
        self.log()
        dt = datetime.datetime.utcnow()
        print("Sequence|IMSI|IMEI|Usage Type|MSISDN|Call date|Call time|Duration(sec)|Bytes Rx|Bytes Tx|2nd Party IMSI|2nd Party MSISDN")
        cdrs = []
        for i in range(cdr_n):
            mnc = random.sample(self.mncs, 1)
            parties = random.sample(mnc[0].subscribers, 2)
            cdr = self.__gen_cdr(parties, i, dt.date(), dt.time())
            dt = dt + datetime.timedelta(microseconds=random.randrange(2000, 8000))
            print("|".join(map(str, cdr)))


    def gen_operators_population(self, operators_n, subscribers_n):
        self.mncs = list()
        for mcc in self.mobile_operators.select_random_mcc(operators_n):
            self.mncs.extend(mcc[1])

        for mnc in self.mncs:
            mnc.generates_subscribers(subscribers_n)

    def log(self):
        for m in self.mncs:
            print(m.iso, m.country_code, m.mcc, m.mnc, m.network)
            for s in m.subscribers:
                print("\t", s)

    def __gen_cdr(self, parties, seq, date, time):
        f,s = parties
        usage,duration,down,up = random_data.random_usage()

        s_imsi = s.imsi if usage != "D" else ""
        s_msisdn = s.msisdn if usage != "D" else ""
        return [seq, f.imsi, f.imei, usage, f.msisdn, date, time, duration, down, up, s_imsi, s_msisdn]




def main():
    if len(sys.argv) < 3:
            print("Usage: ", sys.argv[0], "operators subscribers")
            sys.exit(1)


    op = int(sys.argv[1])
    nn = int(sys.argv[2])
    cdrs = int(sys.argv[3])

    operators = MobileOperators('./mcc-mnc-table.csv')
    gen = Generator(operators)
    gen.generate_cdrs(op, nn, cdrs)





if __name__ == "__main__":
    main()
