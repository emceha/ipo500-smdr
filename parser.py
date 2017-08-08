#! python
#! coding: utf-8

import csv
from datetime import timedelta
from collections import defaultdict


def main(logfile):
    calls = csv.DictReader(open(logfile, encoding='utf-8'))

    ## filter all outgoing external calls
    filtered = [c for c in calls if c['direction'] == 'O' and c['p2name'].startswith('Line')]

    ## filter all outgoing internal calls
    #filtered = [c for c in calls if c['direction'] == 'O' and c['isinternal'] == '1']

    ## for every caller collect pairs (called number, call duration)
    callers = defaultdict(list)
    for call in filtered:
        caller = call['p1name']
        called = call['called']

        (hh, mm, ss) = call['duration'].split(':')
        duration = timedelta(hours=int(hh), minutes=int(mm), seconds=int(ss))

        if duration > timedelta():
            callers[caller].append((called, duration))

    ## present results
    for caller in callers:
        print(caller)
        print('+------------+-----+----------+')

        called = defaultdict(list)
        for number, duration in callers[caller]:
            called[number].append(duration)

        total = timedelta()
        for number in called:
            sd = sum(called[number], timedelta())
            total += sd
            print('| % 10s | % 3s | %  8s |' % (number, len(called[number]), sd))

        print('+------------+-----+----------+')
        print('             | % 3s | % 8s |' % (len(callers[caller]), total))
        print('             +-----+----------+')


if __name__ == "__main__":
    from sys import argv

    if len(argv) > 1:
        main(argv[1])
    