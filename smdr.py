#! /usr/bin/env python3

import os
import logging
from telnetlib import Telnet

HEADER = ("callstart,duration,ring,caller,dir,called,dialled,acc,isinternal,"
          "callid,cont,p1device,p1name,p2device,p2name,hold,park,authvalid,"
          "authcode,ucharged,charge,currency,aocamount,callunits,aocunits,"
          "costperunit,markup,extargcause,extargid,extargeted,"
          "ip1,port1,ip2,port2")

if not os.path.isdir("./log"):
    os.makedirs("./log")

logging.basicConfig(
    filename="./log/smdr.log",
    format="%(levelname)s : %(asctime)s : %(message)s",
    level=logging.INFO)

logging.info("begin ...")

try:
    conn = Telnet('192.168.4.201', 8808)

    while True:
        data = conn.read_until(b'\n', 10).strip()

        if not data:
            break
        else:
            row = data.decode('utf-8')
            year, month = row[:7].split('/')
            filename = f"./log/{year}-{month}.csv"

            if not os.path.exists(filename):
                with open(filename, "w", encoding='utf-8') as clog:
                    clog.write(HEADER + '\n')
                    clog.write(row + '\n')
            else:
                with open(filename, "a", encoding='utf-8') as clog:
                    clog.write(row + '\n')

    logging.info(" ... done")

except Exception:
    logging.exception("aborted")
