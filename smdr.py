'''
ipo set to listen on port 8808
'''

#! /usr/bin/python3
# -*- coding: utf-8 -*-

import os
import logging
from telnetlib import Telnet
from datetime import datetime

header = b"callstart,duration,ring,caller,dir,called,dialled,acc,isinternal," + \
         b"callid,cont,p1device,p1name,p2device,p2name,hold,park,authvalid," + \
         b"authcode,ucharged,charge,currency,aocamount,callunits,aocunits," + \
         b"costperunit,markup,extargcause,extargid,extargeted,ip1,port1,ip2,port2"

if not os.path.isdir('./log'):
    os.makedirs('./log')

logging.basicConfig(filename="./log/smdr.log",
                    format='%(levelname)s : %(asctime)s : %(message)s',
                    level=logging.INFO)

logging.info('begin ...')

rows = 0
try:
    conn = Telnet('192.168.0.201', 8808)  # ipo

    while True:
        data = conn.read_until(b'\n', 10).strip()

        if not data:
            break
        else:
            row = data.decode('utf-8')
            print(row)
            stamp = datetime.strptime(row[:19], '%Y/%m/%d %H:%M:%S')
            filename = "./log/{}-{}.csv".format(stamp.strftime("%Y"),
                                                stamp.strftime("%m"))

            if not os.path.exists(filename):
                with open(filename, "wb") as clog:
                    clog.write(header + b'\n')
                    clog.write(data + b'\n')
            else:
                with open(filename, "ab") as clog:
                    clog.write(data + b'\n')
            rows += 1

    logging.info('done, new rows: {}'.format(rows))

except Exception as err:
    print(str(err))
    logging.exception('aborted')
