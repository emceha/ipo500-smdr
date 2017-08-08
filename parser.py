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
    for call in res:
        caller = call['p1name']
        called = call['called']

        (hh, mm, ss) = call['duration'].split(':')
        td = timedelta(hours=int(hh), minutes=int(mm), seconds=int(ss))

        if td > timedelta():
            d[caller].append((called, td))

    ## present results
    for name in d:
        print(name)
        print('+------------+-----+----------+')

        dd = defaultdict(list)
        for called, duration in d[name]:
            dd[called].append(duration)

        total = timedelta()
        for called in dd:
            sd = sum(dd[called], timedelta())
            total += sd
            print('| % 10s | % 3s | %  8s |' % (called, len(dd[called]), sd))

        print('+------------+-----+----------+')
        print('             | % 3s | % 8s |' % (len(d[name]), total))
        print('             +-----+----------+')


if __name__ == "__main__":
    from sys import argv

    if len(argv) > 1:
        main(argv[1])
    