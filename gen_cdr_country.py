import sys
import csv
import random
import datetime
import argparse
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

    def select_random_mcc_with_population(self, countries_n, subscribers_n, verbose=False):
        return self.generate_cdr_for_countries(random.sample(self.by_mcc.keys(), countries_n), subscribers_n, verbose)

    def select_mccs_with_population(self, mcc_list, subscribers_n, verbose=False):
        return self.generate_cdr_for_countries(mcc_list, subscribers_n, verbose)

    def generate_cdr_for_countries(self, mcc_list, subscribers_n, verbose=False):
        r = []
        for k in mcc_list:
            mobile_operators = self.by_mcc[k]
            if verbose: print(mobile_operators[0].country, mobile_operators[0].mcc, file = sys.stderr)
            carriers_per_mcc = len(mobile_operators)
            population = carriers_per_mcc * subscribers_n
            msin = list(random_data.generate_set( lambda: random_data.msin() , population))
            imei = list(random_data.generate_set( lambda: random_data.imei() , population))
            number = list(random_data.generate_set( lambda: random_data.subscriber_number(9) , population))

            msin_parts = random_data.partition(msin, carriers_per_mcc)
            iemi_parts = random_data.partition(imei, carriers_per_mcc)
            num_parts = random_data.partition(number, carriers_per_mcc)

            for i,mnc in enumerate(mobile_operators):
                if verbose: print(mnc.mnc, mnc.network, file = sys.stderr)
                mnc.attach_subscribers(msin_parts[i], iemi_parts[i], num_parts[i])
                r.append(mnc)
        return r

    def __load_operators(self,file_name):
        with open(file_name, mode='r') as infile:
            reader = csv.reader(infile)
            ops = list(reader)
            return ops[1:] # drop header first line

class Generator:
    def __init__(self, mnc_list):
        self.mncs = mnc_list

    def generate_cdrs_mnc_bound(self, cdr_n, x_carrier_cdrs):
        dt = datetime.datetime.utcnow()
        print("Sequence|IMSI|IMEI|Usage Type|MSISDN|Call date|Call time|Duration(sec)|Bytes Rx|Bytes Tx|2nd Party IMSI|2nd Party MSISDN")
        cdrs = []
        for i in range(cdr_n):
            sameCarrier = random.choices([True, False], [100-x_carrier_cdrs, x_carrier_cdrs])[0]
            if sameCarrier:
                mnc = random.sample(self.mncs, 1)
                parties = random.sample(mnc[0].subscribers, 2)
                print("intra : ", parties[0], "\n\t", parties[1])
            else:
                mnc2 = random.sample(self.mncs, 2)
                s1 = random.sample(mnc2[0].subscribers, 1)[0]
                s2 = random.sample(mnc2[1].subscribers, 1)[0]
                parties = [s1, s2]
                print("inter : ", parties[0], "\n\t", parties[1])

            cdr = self.__gen_cdr(parties, i, dt.date(), dt.time())
            dt = dt + datetime.timedelta(microseconds=random.randrange(2000, 8000))
            print("|".join(map(str, cdr)))

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

def simulate(args):
    # def start(mcc_n, subscribers_n, cdr_n, mcc_list):
    operators = MobileOperators(args.mcc_table_file)
    if args.mcc_n != 0:
        gen = Generator(operators.select_random_mcc_with_population(args.mcc_n, args.population_n, args.verbose_f))
    else:
        gen = Generator(operators.select_mccs_with_population(args.mcc_list, args.population_n, args.verbose_f))
    gen.generate_cdrs_mnc_bound(args.cdr_n, args.x_carrier_cdrs)


def main():
    parser = argparse.ArgumentParser(description='CDR simulator')
    parser.add_argument('cdr_n', action='store', type=int,
                        help='Number of CDRs to generate')

    mcc_group = parser.add_mutually_exclusive_group()
    mcc_group.add_argument('--countries', '-c', action='store', dest='mcc_n', type=int, default=0,
                            help='how many countries to randomly select')
    mcc_group.add_argument('--mcc-list', '-m', action='store', dest='mcc_list', nargs='*', default=['425'],
                            help='list of MCCs to select thier MNCs')

    parser.add_argument('--population', '-p', action='store', dest='population_n', type=int, default=100,
                        help='population of ubscribers per mobile carrier')

    parser.add_argument('--cross-carrier', '-x', action='store', dest='x_carrier_cdrs', type=int, default=0,
                        help='generate cross carrier cdrs probality X_CARRIER_CDRS/100')

    parser.add_argument('--cross-country', '-z', action='store', dest='x_country_cdrs', type=int, default=0,
                        help='generate cross country cdrs')

    parser.add_argument('--verbose', '-v', action='store_true', dest='verbose_f', default=False,
                        help='print simulation parameters to stderr')

    parser.add_argument('--mcc_table', '-f', action='store', dest='mcc_table_file', default='./mcc-mnc-table.csv',
                        help='csv file with mcc mnc data')

    parser.add_argument('--version', action='version', version='%(prog)s 1.0')

    args = parser.parse_args()
    simulate(args)

if __name__ == "__main__":
    main()
