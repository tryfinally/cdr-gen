# CDR generator

Generate randmoly simulated CDR records.

1. The generated CDRs contain real country codes (MCC) and real mobile network codes (MNC).
1. Mobile numbers and MSIN and IMEI are randomly generated.


Sample usage:

```bash
python3 gen_cdr_country.py 1000000 -z 20 -x 50  -c 40
```

Will generate 1 million random call details records from a random selection of 40 countries.\
with a 0.20 chance of international call and a 0.5 chance of domestic call between two mobile networks.


## format of generated CDR

The generated data is composed of records separated by new line.\
Each record describes one mobile call or data transaction and is composed of fields separated by '|'.

### fields

1. Sequence Number
2. Subscriber IMSI
3. Subscriber IMEI
4. Usage Type
5. Subscriber MSISDN
6. Call date
7. Call time
8. Duration in seconds
9. Bytes downloaded
10. Bytes uploaded
11. Second Party IMSI (if MO call or SMS)
12. Second Party MSISDN (if MO call or SMS)

---

## Usage

`python3 gen_cdr_country.py -h`\
Display usage message.

`python3 gen_cdr_country.py 1000 -z 20 -x 40 -m 310 311 312 316`\
Generate 1000 CDRs for calls in US (including Guam) with a 0.2 probability of cross inter-region call.\
And a 0.4 probability of inter-network call.\
Currently US (includeing Guam) has 218 mobile operators.

`python3 gen_cdr_country.py 1000 -m 420 422 424`\
Generate 1000 CDRs for call in Saudi Arabia, Oman and United Arab Emirates.\
All CDRs are for domestic calls with a probability of 0.2 of being cross mobile operator call.

`python3 gen_cdr_country.py 0 -m 234 -v`\
Generate 0 CDRs for UK which has 44 mobile operators. But list all MNC codes for mobile operators in UK.

`python3 gen_cdr_country.py 100000 -c 13 -x 25 -v`\
Generate 100,000 CDRs for local calls in a random selection of 13 countries.\
Generated calls have a 0.25 probability of cross operator call in the same country.\
and print on stdandard error details of countries selected and their mobile operators.

`python3 gen_cdr_country.py 1000 -z 20 -x 50  -c 10`\
Generate 1000 CDRs occurring a random selection of 10 countries with a 0.2 probability of an international call\
and a probability of 0.5 for cross operator if the call is inside the selected country.

`python3 gen_cdr_country.py 100000 -z 5 -x 25 -m 530 262 424`\
Generate 100,000 CDRs for calls in New Zealand, Germany and United Arab Emirates where the probability of an\
international call is 0.05 and the probability of cross operator call inside the same country is 0.25.
