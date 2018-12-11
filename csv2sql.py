#! /usr/bin/env python3

import sys
import os
import csv
import sqlite3
import hashlib
from datetime import datetime


COLUMNS = ("callstart,duration,ring,caller,dir,called,dialled,acc,"
           "isinternal,callid,cont,p1device,p1name,p2device,p2name,"
           "hold,park,authvalid,authcode,ucharged,charge,currency,"
           "aocamount,callunits,aocunits,costperunit,markup,"
           "extargcause,extargid,extargeted,ip1,port1,ip2,port2,"
           "calluid")


def row_exists(conn, crsr, cuid):
    query = f"SELECT calluid FROM calls WHERE calluid=?"
    crsr.execute(query, (cuid,))
    fetch = crsr.fetchall()
    conn.commit()
    return fetch


def insert_row(conn, crsr, columns, values, row):
    query = f"INSERT INTO calls({columns}) VALUES({values})"
    crsr.execute(query, row)
    conn.commit()


def create_table(conn, crsr, columns):
    query = f"CREATE TABLE IF NOT EXISTS calls ({columns})"
    crsr.execute(query)
    conn.commit()


def make_cuid(row):
    cstr = f"{row[0]} {row[1]} {row[8]} {row[9]}"
    cuid = hashlib.md5(cstr.encode("ascii")).hexdigest()
    return cuid


def csv_to_sql(db, csvfile):
    with sqlite3.connect(db) as conn:
        crsr = conn.cursor()

        with open(csvfile, 'r', encoding="utf-8") as clog:
            reader = csv.reader(clog)
            next(reader)
            strcols = COLUMNS
            cols = strcols.split(',')
            create_table(conn, crsr, strcols)

            for row in reader:
                cuid = make_cuid(row)
                if not row_exists(conn, crsr, cuid):
                    dt = row[0].replace('/', '-')
                    row[0] = int(datetime.fromisoformat(dt).timestamp())
                    row.append(cuid)
                    values = ','.join('?' * len(cols))
                    insert_row(conn, crsr, strcols, values, row)


def main(dbpath, flist):
    try:
        for cf in flist:
            sys.stdout.write(f'{cf} ... ')
            sys.stdout.flush()
            csv_to_sql(dbpath, cf)
            sys.stdout.write('OK\n')
    except Exception as error:
        print(error)


if __name__ == "__main__":
    if sys.argv[1:]:
        main('./db/smdr.db', sys.argv[1:])
