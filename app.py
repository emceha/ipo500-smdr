#! python3
#! coding: utf-8

import csv
import os
import time
from collections import defaultdict
from datetime import timedelta
from bottle import Bottle, static_file, template

app = Bottle()
logspath = './log'


@app.route('/')
def check_logs():
    result = []
    for f in os.listdir(logspath):
        if f != 'smdr.log':
            result.append((os.path.join(logspath, f), f[:-4]))
    return template('index', data=result)


@app.route('/dsp/<logfile:path>')
def dsp_log(logfile):
    with open(logfile, encoding='utf-8', errors='replace') as clog:
        result = clog.read()   
    return template('simple', data=result)


@app.route('/calls/<logfile:path>')
def dsp_sheet(logfile):
    with open(logfile, encoding='utf-8') as clog:
        calls = [row.split(',')[:15] for row in clog.readlines()]
    return template('calls', data=calls)


@app.route('/stats/<filtr>/<logfile:path>')
def dsp_stats(logfile, filtr):
    calls = csv.DictReader(open(logfile, encoding='utf-8'))
    time.sleep(1)   
    if filtr == "ext":
        filtered = (c for c in calls if c['dir'] == 'O' and
                    len(c['called']) > 8 and
                    c['p2name'].startswith('Line'))

    elif filtr == "int":
        filtered = (c for c in calls if c['dir'] == 'O' and c['isinternal'] == '1')
        
    else:
        filtered = ()

    callers = defaultdict(list)
    name = defaultdict(str)
    for call in filtered:
        caller = call['p1name']
        called = call['called']

        (hh, mm, ss) = call['duration'].split(':')
        duration = timedelta(hours=int(hh), minutes=int(mm), seconds=int(ss))

        if duration > timedelta():
            name[called] = call['p2name']
            callers[caller].append((called, duration))

    tables = []
    for caller in callers:
        subtab = []
        subtab.append((caller, ' ', ' '))
        
        called = defaultdict(list)
        for number, duration in callers[caller]:
            called[number].append(duration)

        total = timedelta()
        for number in called:
            sd = sum(called[number], timedelta())
            total += sd
            p2 = number if filtr == "ext" else name[number]
            subtab.append((p2, len(called[number]), '%s' % sd))

        if len(subtab) > 2:
            subtab.append((' ', len(callers[caller]), '%s' % total))
        tables.append(subtab)

    return template('stats', data=tables)


@app.get('/404.png')
def get_page():
    return static_file('404.png', root='./static')


@app.error(404)
def error404(error):
    return template('404')


@app.error(500)
def error500(error):
    return template('404')


@app.get('/favicon.ico')
def get_favicon():
    return static_file('favicon.ico', root='./static')


@app.get('/style.css')
def get_css():
    return static_file('style.css', root='./static')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8877, debug=True)
