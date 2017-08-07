#! python
#! coding: utf-8

import csv
from datetime import timedelta
from collections import defaultdict


def main(logfile):
    calls = csv.DictReader(open(logfile, encoding='utf-8'))
    
    ## filter all outgoing external calls
    res = [c for c in calls if c['direction'] == 'O' and c['p2name'].startswith('Line')]

    ## filter all outgoing internal calls
    #res = [c for c in calls if c['direction'] == 'O' and c['isinternal'] == '1']

    ## for every caller collect pairs (called number, call duration)
    d = defaultdict(list)
    for n in res:
        caller = n['p1name']
        called = n['called']

        (h, m, s) = n['duration'].split(':')
        delta = timedelta(hours=int(h), minutes=int(m), seconds=int(s))

        if delta > timedelta():
            d[caller].append((called, delta))

    ## present results
    for n in d:
        print(n)
        print('+-----------+-----+----------+')

        dd = defaultdict(list)
        for k, v in d[n]:
            dd[k].append(v)

        total = timedelta()
        for k in dd:
            sd = sum(dd[k], timedelta())
            total += sd
            print('| % 9s | % 3s | %  8s |' % (k, len(dd[k]), sd))

        print('+-----------+-----+----------+')
        print('            | % 3s | % 8s |' % (len(d[n]), total))
        print('            +-----+----------+')


if __name__ == "__main__":
    from sys import argv

    if len(argv) > 1:    
        main(argv[1])

