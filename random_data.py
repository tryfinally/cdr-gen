import random
import string
import datetime

def digits(begin, end):
        return str(random.randrange(begin, end + 1))

def get_random_string(length):
    return ''.join(random.choice(string.ascii_letters) for i in range(length))

def subscriber_number(length):
    return ''.join(random.choice(string.digits) for i in range(length))

def imei():
    a =  ''.join(random.choice(string.digits) for i in range(2))
    b = ''.join(random.choice(string.digits) for i in range(5))
    c = ''.join(random.choice(string.digits) for i in range(7))
    return a + '-' + b + '-' + c

def msin():
    return ''.join(random.choice(string.digits) for i in range(10))


def date(start_date, end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    return random_date

def generate_set(gen, n):
    s = set()
    while len(s) < n:
        s.add(gen())
    return s

def random_usage():
    u =  random.choice(["MOC", "MTC", "SMS-O", "SMS-MT", "D"])
    upload = 0
    download = 0
    duration = 0
    if u == "D":
        upload = random.randrange(512, 1024*1024/2)
        download = random.randrange(1024, 10*1024*1024)
    if u == "MOC" or u == "MTC":
        duration = random.randrange(20, 1200)

    return (u, duration, download, upload)

def partition(list_in, n):
    random.shuffle(list_in)
    return [list_in[i::n] for i in range(n)]
