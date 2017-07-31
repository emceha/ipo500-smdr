#! python
# not compatible with python 3!

from telnetlib import Telnet
from datetime import datetime
import logging
import os

header = "DATETIME,DURATION,RING,CALLER,DIR,CALLED,DIALED,ACC,EXT,CALLID,CONT,P1DEV,P1NAME,P2DEV,P2NAME,,,,,,,,,,,,,,,,IP1,PORT1,IP2,PORT2\n"
count, lines = 0, 0
logging.basicConfig(filename="smdr.log", format='%(levelname)s : %(asctime)s : %(message)s', level=logging.INFO)
logging.info('begin ...')

conn = Telnet('192.168.0.201', 8808) # ipo

try:
    while count < 5:
        data = conn.read_until('\n', 3) # 3s timeout
        
        if data != "":
            stamp = datetime.strptime(data[:19], '%Y/%m/%d %H:%M:%S')
            print(data)
    
            filename = "%s-%s.log" % (stamp.strftime("%Y"), stamp.strftime("%m"))
            if not os.path.exists(filename):
                with open(filename, "w") as clog:
                    clog.write(header)
                    clog.write(data)
            else:
                with open(filename, "a") as clog:
                    clog.write(data)
        
            lines += 1
            count = 0
        else:
            count += 1
    
    logging.info('end, new records : %s' % lines)

except Exception as err:
    print(str(err))
    logging.exception('aborted')
