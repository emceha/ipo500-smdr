#! python
#! coding: utf-8

import pandas as pd


def main(logfile):
    df = pd.read_csv(logfile, sep=',')
    df['duration'] = pd.to_timedelta(df['duration'])

    df = df.loc[(df.direction == 'O') & df.p2name.str.startswith("Line") &
                 (df.duration > pd.to_timedelta(0))]

    print(df.groupby(['p1name', 'called'])['duration'].sum())


if __name__ == "__main__":
    from sys import argv

    if len(argv) > 1:
        main(argv[1])
