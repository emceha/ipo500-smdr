#! python3
#! coding: utf-8

from telnetlib import Telnet
from datetime import datetime
import logging
import os

header = "DATETIME,DURATION,RING,CALLER,DIR,CALLED,DIALED,ACC,EXT,CALLID,\
          CONT,P1DEV,P1NAME,P2DEV,P2NAME,,,,,,,,,,,,,,,,IP1,PORT1,IP2,PORT2"

count, lines = 0, 0

logging.basicConfig(filename="log\\smdr.log",
                    format='%(levelname)s : %(asctime)s : %(message)s',
                    level=logging.INFO)

logging.info('begin ...')

try:
    conn = Telnet('192.168.0.201', 8808) # ipo

    while count < 5: # 15s total timeout
        data = conn.read_until(b'\n', 3).decode("utf-8").strip() # 3s timeout

        if data != "":
            print(data)

            stamp = datetime.strptime(data[:19], '%Y/%m/%d %H:%M:%S')
            filename = "log\\%s-%s.log" % (stamp.strftime("%Y"), stamp.strftime("%m"))
            
            if not os.path.exists(filename):
                with open(filename, "w") as clog:
                    clog.write(header + '\n')
                    clog.write(data + '\n')
            else:
                with open(filename, "a") as clog:
                    clog.write(data + '\n')

            lines += 1
            count = 0
        else:
            count += 1

    logging.info('end, new records : %s' % lines)

except Exception as err:
    print(str(err))
    logging.exception('aborted')
