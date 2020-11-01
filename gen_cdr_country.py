import sys
import csv
import random_data

class MobileOperator:
    def __init__(self, record):
        self.mcc = record[0]
        self.mnc = record[2]
        self.iso = record[4]
        self.country = record[5]
        self.country_code = record[6]
        self.network = record[7]

class MobileOperators:
    def __init__(self, file_name):
        self.operators = self.__load_operators(file_name)
        self.by_mcc = {}
        for row in self.operators:
            self.by_mcc.setdefault(row[0], []).append(MobileOperator(row))

    def get_operators_by_country(self, mcc):
        return self.by_mcc[mcc]

    def __load_operators(self,file_name):
        with open(file_name, mode='r') as infile:
            reader = csv.reader(infile)
            ops = list(reader)
            return ops[1:] # drop header first line

def main():
    if len(sys.argv) < 2:
            print("Usage: ", sys.argv[0], "country_code")
            sys.exit(1)

    cc = sys.argv[1]
    operators = MobileOperators('./mcc-mnc-table.csv')
    country = operators.get_operators_by_country(cc)

    for c in country:
        print(c.iso, c.country_code, c.mcc, c.mnc, c.network, c.country)


if __name__ == "__main__":
    main()
