#! /usr/bin/env python3

import os
import logging
import sqlite3
import hashlib
from telnetlib import Telnet
from datetime import datetime


COLUMNS = ("callstart,duration,ring,caller,dir,called,dialled,acc,"
           "isinternal,callid,cont,p1device,p1name,p2device,p2name,"
           "hold,park,authvalid,authcode,ucharged,charge,currency,"
           "aocamount,callunits,aocunits,costperunit,markup,"
           "extargcause,extargid,extargeted,ip1,port1,ip2,port2,"
           "calluid")


logging.basicConfig(
    format="%(asctime)s [ %(levelname)-6s] %(message)s ",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO
)


def create_table(conn, crsr):
    query = f"CREATE TABLE IF NOT EXISTS calls ({COLUMNS})"
    crsr.execute(query)
    conn.commit()


def get_row(adrs, port):
    with Telnet(adrs, port, 15) as conn:
        row = conn.read_until(b'\n', 10).strip()
    return row.decode('utf-8')


def insert_row(conn, crsr, row):
    values = ','.join('?' * len(row))
    query = f"INSERT INTO calls({COLUMNS}) VALUES({values})"
    crsr.execute(query, row)
    conn.commit()


def make_cuid(row):
    cstr = f"{row[0]} {row[1]} {row[8]} {row[9]}"
    cuid = hashlib.md5(cstr.encode("ascii")).hexdigest()
    return cuid


def main(db, address, port):
    try:
        with sqlite3.connect(db) as conn:
            crsr = conn.cursor()
            logging.info(f"database : '{db}'")
            create_table(conn, crsr)
            logging.info(f"ipo : {address}:{port}")

            while True:
                row = get_row(address, port)
                if not row:
                    break

                row = row.split(',')
                cuid = make_cuid(row)
                row.append(cuid)

                row[0] = row[0].replace('/', '-')
                insert_row(conn, crsr, row)
                logging.info(f"{cuid}")

        logging.info("... done ")
    except Exception as error:
        logging.error(error)


if __name__ == "__main__":
    main('./db/smdr.db', '192.168.4.201', 8808)
