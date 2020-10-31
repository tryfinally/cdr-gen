#!/usr/bin/env python3
import sys
import random
import string
import datetime

def get_random_digits(begin, end):
        return str(random.randrange(begin, end + 1))

def get_random_string(length):
    return ''.join(random.choice(string.ascii_letters) for i in range(length))

def get_random_phone(length):
    return ''.join(random.choice(string.digits) for i in range(length))

def get_random_imei():
    a =  ''.join(random.choice(string.digits) for i in range(2))
    b = ''.join(random.choice(string.digits) for i in range(5))
    c = ''.join(random.choice(string.digits) for i in range(7))
    return a + '-' + b + '-' + c


def random_date(start_date, end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    return random_date


def generate_operators(countries, operators):
    names = set()
    while len(names) != countries * operators:
        names.add(get_random_string(12))

    mcc_mnc = set()
    for c in range(countries):
        mcc = get_random_digits(2, 6) + get_random_digits(10, 21)
        many_ops = random.randrange(int(operators*0.8), int(operators*1.2))
        for n in range(many_ops):
            mnc = get_random_digits(1, 21)
            mnc = mnc if len(mnc) == 2 else '0' + mnc
            mcc_mnc.add(mcc + mnc)

    # print(mcc_mnc)
    return dict(zip(mcc_mnc, names))

def random_usage():
    u =  random.choice(["MOC", "MTC", "SMS-O", "SMS-MT", "D" ])
    upload = 0
    download = 0
    duration = 0
    if u == "D":
        upload = random.randrange(512, 1024*1024/2)
        download = random.randrange(1024, 10*1024*1024)
    if u == "MOC" or u == "MTC":
        duration = random.randrange(20, 1200)

    return (u, duration, download, upload)


def generates_subscribers(ops, number):
    pop_size = number/len(ops)
    # print("pop size", pop_size)
    all_subscribers = []
    for op in ops:
        subscribers = set()
        # i = 0
        if pop_size >= 10:
            subscribers_size = random.randrange(int(pop_size*0.5) , int(pop_size*1.5))
        else:
            subscribers_size = random.randrange(1, 10)
        while len(subscribers) < subscribers_size:
            subscriber = (op + '0' + get_random_phone(10), get_random_imei())
            subscribers.add( subscriber )
        # print("pop for op ", op, " ", len(subscribers))
        all_subscribers.extend( list(map(tuple, subscribers)) )

    # print("pop of all subscribers ", len(all_subscribers))
    return all_subscribers

def select_secondary(subscribers, sub):
    s = random.choice(subscribers)
    while s[0] == sub:
        s = random.choice(subscribers)
    return s[0][3:]

def generate_cdrs(c, o, n, start_date):
    ops = generate_operators(c, o)
    subscribers = generates_subscribers(ops, n//4)

    current = start_date
    for i in range(n):
        seq = str(i)
        sub = random.choice(subscribers)
        msisdn = sub[0]
        imei = sub[1]
        usage,duration,down, up = random_usage()

        second_party = select_secondary(subscribers, sub) if usage != "D" else ""
        current = current + datetime.timedelta(seconds=random.randrange(0, 3))
        r = [i, msisdn, imei, usage, msisdn[3:], current.date(), current.time(), duration , down, up, second_party]
        r = map(str, r)
        line = "|".join(r)
        print(line)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: ", sys.argv[0], "countries operator/countries subscribers")
        sys.exit(1)
    c = int(sys.argv[1])
    o = int(sys.argv[2])
    n = int(sys.argv[3])
    generate_cdrs(c, o, n, datetime.datetime(2020, 10, 1, 00, 00))
