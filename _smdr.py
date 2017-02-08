#! python

from telnetlib import Telnet
from datetime import datetime
import logging

count, lines = 0, 0

logging.basicConfig(filename="smdr.log", format='%(levelname)s : %(asctime)s : %(message)s', level=logging.INFO)
logging.info('begin ...')

conn = Telnet('192.168.0.201', 8808) # ipo address and port 

try:
    while count < 4:
        smdr = conn.read_until('\n', 5) # 5s timeout
        
        if smdr != "":
            data = smdr.strip().split(',')
            stamp = datetime.strptime(data[0], '%Y/%m/%d %H:%M:%S')
            data = ','.join(data[0].split(' ') + data[1:]) # separate date and time
            print(data)
            
            filename = "%s-%s.log" % (stamp.strftime("%Y"), stamp.strftime("%m")) 
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
