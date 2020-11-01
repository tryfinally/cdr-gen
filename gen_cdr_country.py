import sys
import csv

class MobileOperators:
    def __init__(self, file_name):
        self.operators = self.__load_operators(file_name)
        self.by_mcc = {rows[0]:rows[0:] for rows in self.operators}

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
    print(operators.get_operators_by_country(cc))


if __name__ == "__main__":
    main()
