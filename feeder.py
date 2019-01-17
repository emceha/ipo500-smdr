#! /usr/bin/env python3

import sys
import sqlite3
import hashlib
import logging

CNAMES = ("callstart,duration,ring,caller,dir,called,dialled,acc,"
          "isinternal,callid,cont,p1device,p1name,p2device,p2name,"
          "hold,park,authvalid,authcode,ucharged,charge,currency,"
          "aocamount,callunits,aocunits,costperunit,markup,"
          "extargcause,extargid,extargeted,ip1,port1,ip2,port2,"
          "cheksum")


logging.basicConfig(
    format="%(asctime)s [ %(levelname)-6s] %(message)s ",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO)


def insert_row(conn, crsr, row):
    values = ','.join('?' * len(row))
    query = f"INSERT OR IGNORE INTO calls({CNAMES}) VALUES({values})"
    crsr.execute(query, row)
    conn.commit()


def progress(fname, all_rows, cur_row):
    prct = cur_row * 100 // all_rows
    pbar = "#" * (prct // 4) + "-" * (25 - (prct // 4))
    print(f"\r{fname:<20} {cur_row:5} [{pbar}] {prct:3}% ",
          end="", flush=True)


def csv_to_sql(db, csv):
    with sqlite3.connect(db) as conn:
        crsr = conn.cursor()

        with open(csv, 'rb') as clog:
            rows = clog.readlines()

        if rows and (rows[0].startswith(b'callstart') or
                     rows[0].startswith(b'\xef\xbb\xbf')):
            rows = rows[1:]

        try:
            for n, row in enumerate(rows):
                row = row.strip()
                chksum = hashlib.sha1(row).hexdigest()
                row = row.decode().replace('/', '-').split(',')
                row.append(chksum)
                progress(csv, len(rows), n + 1)
                insert_row(conn, crsr, row)
        except KeyboardInterrupt:
            sys.exit("\r")
        except Exception as error:
            logging.error(error)


def main(dbpath, fpath):
    try:
        for cf in fpath:
            csv_to_sql(dbpath, cf)
            print()
    except Exception as error:
        logging.error(error)


if __name__ == "__main__":
    if sys.argv[1:]:
        main('./db/smdr.db', sys.argv[1:])
