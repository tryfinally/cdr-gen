# CDR generator

generate random CDR files

use to generate files containing random call details records.
Usage:

```bash
generator.py 40 10 1000000
```

will generate 1 million random call details records from a population of
40 countries, ~10 mobile carriers per country.
The generated file will contain usage records from about 1/4 million unique subscribers.

```bash
generator.py 40 10 1000000 > data.cdr
cat data.cdr | cut -d'|' -f2 | sort | uniq | wc -l
```

## format
The gnerated data is composed from records seprated by new line.
Each record describes one usage and is composed of fields seprated by '|'.

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

# Usage

sample runs:
-
`python3 gen_cdr_country.py -h`\
display usage message.

`python3 gen_cdr_country.py 1000 -m 420 -x 40`
generate 1000 CDRs for MCC 420 - Saudi Arabia
with 0.4 probality of cross MNC CDRs. Saui Arabia has 6 mobile operators.

`python3 gen_cdr_country.py 10 -m 420 422`\
generate 10 CDRs for MCC: 420, 422  (Saudi Arabia and Oman).\
All CDRs ar intra MNC

`python3 gen_cdr_country.py 0 -m 234 -v`\
generate 0 CDRs for UK which has 44 mobile operators. But list all MNC codes for operators in UK.

`python3 gen_cdr_country.py 100000 -c 13 -x 20 -v`\
generate 100,000 CDRs for a random selection of 13 countries. With a probality of inter MNC CDR of 20/100. Also, print on stderr details of countries selected.

`python3 gen_cdr_country.py 1000 -z 20 -x 50  -c 10`\
generate 1000 CDRs occuring a random selection of 10 countries with a 0.2 probability of international call (cross contry)
and a probality of 0.5 for cross operator if the call is inside selected country.

`python3 gen_cdr_country.py 100000 -z 5 -x 25 -m 530 262 422`\
generate 100,000 CDRs for calls in New Zeland, germany and United Arab Emirates where the probability of interbational call is 0.05 and the probability of cross operator call inside same country is 0.25.
