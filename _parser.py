#! python
#! coding: utf-8

import sys
import csv
from datetime import timedelta
from collections import defaultdict

# must be the first line of csv file
# DATETIME,DURATION,RING,CALLER,DIR,CALLED,DIALED,ACC,EXT,CALLID,CONT,P1DEV,P1NAME,P2DEV,P2NAME,,,,,,,,,,,,,,,,IP1,PORT1,IP2,PORT2

def main(logfile):
    calls = csv.DictReader(open(logfile))

    # filter all outgoing external calls 
    res = [c for c in calls if c['DIR'] == 'O' and c['P2NAME'].startswith('Line')]
    
    # for every caller collect pairs (phone number, call duration)
    d = defaultdict(list)
    for n in res:
        caller = n['P1NAME']
        called = n['CALLED']
        
        (h, m, s) = n['DURATION'].split(':')
        delta = timedelta(hours=int(h), minutes=int(m), seconds=int(s))

        if delta > timedelta():
            d[caller].append((called, delta))

    # present results
    for n in d:
        print n
        print '+-----------+-----+----------+'
  
        dd = defaultdict(list)
        for k, v in d[n]:
            dd[k].append(v)

        total = timedelta()
        for k in dd:
            sd = sum(dd[k], timedelta())
            total += sd
            print '| % 9s | % 3s | %  8s |' % (k, len(dd[k]), sd)

        print '+-----------+-----+----------+'
        print '            | % 3s | % 8s |' % (len(d[n]), total)
        print '            +-----+----------+'

  
if __name__ == "__main__":
    if len(sys.argv) > 1:    
        main(sys.argv[1])
