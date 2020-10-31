# cdr-gen

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
