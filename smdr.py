#! /usr/bin/env python

import os
import logging
from telnetlib import Telnet

HEADER = b"callstart,duration,ring,caller,dir,called,dialled,acc," + \
         b"isinternal,callid,cont,p1device,p1name,p2device,p2name," + \
         b"hold,park,authvalid,authcode,ucharged,charge,currency," + \
         b"aocamount,callunits,aocunits,costperunit,markup," + \
         b"extargcause,extargid,extargeted,ip1,port1,ip2,port2"

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
            filename = "./log/{}-{}.csv".format(year, month)

            if not os.path.exists(filename):
                with open(filename, "wb") as clog:
                    clog.write(HEADER + b'\n')
                    clog.write(data + b'\n')
            else:
                with open(filename, "ab") as clog:
                    clog.write(data + b'\n')

    logging.info(" ... done")

except Exception:
    logging.exception("aborted")
