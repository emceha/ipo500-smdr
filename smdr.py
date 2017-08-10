#! python3
#! coding: utf-8

from telnetlib import Telnet
from datetime import datetime
import logging
import os

header = b"datetime,duration,ringtime,caller,direction,called,dialled,account,isinternal,callid," + \
         b"cont,p1device,p1name,p2device,p2name,holdtime,parktime,authvalid,authcode,usercharged," + \
         b"callcharge,currency,aocamount,callunits,aocunits,costperunit,markup,exttargettingcause," + \
         b"exttargeterid,exttargetednumber,ip1,port1,ip2,port2"

counter, rows = 0, 0

if not os.path.isdir('./log'):
        os.makedirs('./log')

logging.basicConfig(filename="./log/smdr.log",
                    format='%(levelname)s : %(asctime)s : %(message)s',
                    level=logging.INFO)

logging.info('begin ...')

try:
    conn = Telnet('192.168.0.201', 8808) # ipo

    while counter < 5: # 15s total timeout
        data = conn.read_until(b'\n', 3).strip() # 3s timeout

        if data:
            row = data.decode('utf-8')
            print(row)
            stamp = datetime.strptime(row[:19], '%Y/%m/%d %H:%M:%S')
            filename = "./log/{}-{}.log".format(stamp.strftime("%Y"), stamp.strftime("%m"))

            if not os.path.exists(filename):
                with open(filename, "wb") as clog:
                    clog.write(header + b'\n')
                    clog.write(data + b'\n')
            else:
                with open(filename, "ab") as clog:
                    clog.write(data + b'\n')

            rows += 1
            counter = 0
        else:
            counter += 1

    logging.info('end, new rows : %s' % rows)

except Exception as err:
    print(str(err))
    logging.exception('aborted')
