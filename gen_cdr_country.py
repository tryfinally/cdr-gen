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
        self.subscribers = []

    def generates_subscribers(self, n):
        msin = list(random_data.generate_set( lambda: random_data.msin() , n))
        imei = list(random_data.generate_set( lambda: random_data.imei() , n))
        number = list(random_data.generate_set( lambda: random_data.subscriber_number(9) , n))
        for i in range(n):
            imsi = self.mcc + self.mnc + msin[i]
            msisdn = self.country_code + '0' + number[i]
            self.subscribers.append(Subscriber(msin[i], imei[i], imsi, msisdn))

    def attach_subscribers(self, msins, iemis, numbers):
        assert len(msins) == len(numbers)
        for i in range(len(msins)):
            imsi = self.mcc + self.mnc + msins[i]
            msisdn = self.country_code + '0' + numbers[i]
            self.subscribers.append(Subscriber(msins[i], iemis[i], imsi, msisdn))

class MobileOperators:
    def __init__(self, file_name):
        self.operators = self.__load_operators(file_name)
        self.by_mcc = {}
        for row in self.operators:
            self.by_mcc.setdefault(row[0], []).append(MobileOperator(row))

    def get_operators_by_country(self, mcc):
        return self.by_mcc[mcc]

    def select_random_mcc_with_population(self, countries_n, subscribers_n):
        r = []
        for k in random.sample(self.by_mcc.keys(), countries_n):
            mobile_operators = self.by_mcc[k]
            print(mobile_operators[0].country)
            carriers_per_mcc = len(mobile_operators)
            population = carriers_per_mcc * subscribers_n
            msin = list(random_data.generate_set( lambda: random_data.msin() , population))
            imei = list(random_data.generate_set( lambda: random_data.imei() , population))
            number = list(random_data.generate_set( lambda: random_data.subscriber_number(9) , population))

            msin_parts = random_data.partition(msin, carriers_per_mcc)
            iemi_parts = random_data.partition(imei, carriers_per_mcc)
            num_parts = random_data.partition(number, carriers_per_mcc)

            for i,mnc in enumerate(mobile_operators):
                print(mnc.mnc, mnc.network)
                mnc.attach_subscribers(msin_parts[i], iemi_parts[i], num_parts[i])
                r.append(mnc)
        return r

    def __load_operators(self,file_name):
        with open(file_name, mode='r') as infile:
            reader = csv.reader(infile)
            ops = list(reader)
            return ops[1:] # drop header first line

class Generator:
    def __init__(self, operators):
        self.mobile_operators = operators

    def generate_cdrs_mnc_bound(self, mcc_n, subscribers_n, cdr_n):
        self.mncs = self.mobile_operators.select_random_mcc_with_population(mcc_n, subscribers_n)
        dt = datetime.datetime.utcnow()
        print("Sequence|IMSI|IMEI|Usage Type|MSISDN|Call date|Call time|Duration(sec)|Bytes Rx|Bytes Tx|2nd Party IMSI|2nd Party MSISDN")
        cdrs = []
        for i in range(cdr_n):
            mnc = random.sample(self.mncs, 1)
            parties = random.sample(mnc[0].subscribers, 2)
            cdr = self.__gen_cdr(parties, i, dt.date(), dt.time())
            dt = dt + datetime.timedelta(microseconds=random.randrange(2000, 8000))
            print("|".join(map(str, cdr)))

    def gen_operators_population(self, mcc_n, subscribers_n):
        self.mncs = self.mobile_operators.select_random_mcc_with_population(mcc_n, subscribers_n)

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

def start(mcc, nn, cdrs):
    operators = MobileOperators('./mcc-mnc-table.csv')
    gen = Generator(operators)
    gen.generate_cdrs_mnc_bound(mcc, nn, cdrs)

def main():
    if len(sys.argv) < 3:
            print("Usage: ", sys.argv[0], "countries subscribers cdrs")
            sys.exit(1)

    mcc = int(sys.argv[1])
    nn = int(sys.argv[2])
    cdrs = int(sys.argv[3])
    start(mcc, nn, cdrs)

if __name__ == "__main__":
    main()
    # start(1, 10, 0)
