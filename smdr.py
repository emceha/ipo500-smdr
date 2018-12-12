#! /usr/bin/env python3

import os
import logging
import sqlite3
import hashlib
from telnetlib import Telnet
from datetime import datetime


CNAMES = ("callstart,duration,ring,caller,dir,called,dialled,acc,"
          "isinternal,callid,cont,p1device,p1name,p2device,p2name,"
          "hold,park,authvalid,authcode,ucharged,charge,currency,"
          "aocamount,callunits,aocunits,costperunit,markup,"
          "extargcause,extargid,extargeted,ip1,port1,ip2,port2,"
          "cheksum")

DATATYPES = ("TEXT,TEXT,INTEGER,TEXT,TEXT,TEXT,TEXT,TEXT,INTEGER,"
             "INTEGER,TEXT,TEXT,TEXT,TEXT,TEXT,TEXT,TEXT,TEXT,TEXT,"
             "TEXT,TEXT,TEXT,TEXT,TEXT,TEXT,TEXT,TEXT,TEXT,TEXT,TEXT,"
             "TEXT,INTEGER,TEXT,INTEGER,TEXT NOT NULL UNIQUE")

COLUMNS = ','.join([f"{c} {d}" for c, d in zip(
    CNAMES.split(','), DATATYPES.split(','))])


logging.basicConfig(
    format="%(asctime)s [ %(levelname)-6s] %(message)s ",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO
)


def create_table(conn, crsr):
    crsr.execute(f"CREATE TABLE IF NOT EXISTS calls({COLUMNS});")
    conn.commit()


def get_row(adrs, port):
    with Telnet(adrs, port, 15) as conn:
        row = conn.read_until(b'\n', 10).strip()
    return row


def insert_row(conn, crsr, row):
    values = ','.join('?' * len(row))
    query = f"INSERT INTO calls({CNAMES}) VALUES({values})"
    crsr.execute(query, row)
    conn.commit()


def main(db, log, address, port):
    try:
        with sqlite3.connect(db) as conn:
            crsr = conn.cursor()
            create_table(conn, crsr)

            logging.info(f"database : '{db}'")
            logging.info(f"ipo : {address}:{port}")

            with open(log, 'ab') as bkp:
                while True:
                    row = get_row(address, port)
                    if not row:
                        break

                    bkp.write(row + b'\n')
                    chksum = hashlib.sha1(row).hexdigest()

                    row = row.decode().replace('/', '-').split(',')
                    row.append(chksum)

                    insert_row(conn, crsr, row)

        logging.info("... done")
    except Exception as error:
        logging.error(error)


if __name__ == "__main__":
    main('./db/smdr.db', './log/calls.log', '192.168.4.201', 8808)
