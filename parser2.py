#! python
#! coding: utf-8

import pandas as pd

def main(logfile):
    df = pd.read_csv('log\\2017-08.log', sep=',')
    df['duration'] = pd.to_timedelta(df['duration'])
    
    dfo = df.loc[(df.direction == 'O') & 
                  df.p2name.str.startswith("Line") & 
                 (df.duration > pd.to_timedelta(0))]

    print(dfo.groupby(['p1name', 'called'])['duration'].sum())

if __name__ == "__main__":
    from sys import argv

    if len(argv) > 1:
        main(argv[1])

