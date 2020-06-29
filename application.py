import os
from flask import Flask, request
from flask.templating import render_template
import sqlite3
import time
import numpy as np

app = Flask(__name__)
# port = int(os.getenv("PORT", 5000))


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home_redirect():
    data, timediff = getData()
    if request.method == 'POST':
        if request.form['point'] == 'depseg':

            conn = sqlite3.connect('data/test.db')
            c = conn.cursor()
            if request.form["dep1"] == "":
                mindep = 0
            else:
                mindep = float(request.form["dep1"])
            if request.form["dep2"] == "":
                maxdep = 10000
            else:
                maxdep = float(request.form["dep2"])
            if request.form["seg"] == "":
                seg = 0
            else:
                seg = float(request.form["seg"])
            x = []
            y = []
            while mindep < maxdep:
                if mindep + seg < maxdep:
                    max = mindep + seg
                else:
                    max = maxdep
                x.append(str(mindep) + "-" + str(max))
                c.execute("SELECT * FROM all_month WHERE depth>=? and depth<?", (mindep, max))
                y.append(len(c.fetchall()))
                mindep += seg
            conn.close()
            return render_template('bar.html', x=x, y=y)
        elif request.form['point'] == 'scatter':
            conn = sqlite3.connect('data/test.db')
            c = conn.cursor()
            mindep = float(request.form['dep1'])
            maxdep = float(request.form['dep2'])
            alldata = c.execute("SELECT * FROM all_month WHERE depth>=? and depth<?", (mindep, maxdep))
            demadata = []
            for d in alldata:
                small = []
                small.append(d[3])
                small.append(d[4])
                demadata.append(small)
            conn.close()
            return render_template('scatter.html', data=demadata)

        elif request.form['point'] == 'deppie':
            conn = sqlite3.connect('data/test.db')
            c = conn.cursor()
            mindep = float(request.form["dep1"])
            maxdep = float(request.form["dep2"])
            seg = float(request.form["seg"])
            x = []
            y = []
            while mindep < maxdep:
                if mindep + seg < maxdep:
                    max = mindep + seg
                else:
                    max = maxdep
                x.append(str(mindep) + "-" + str(max))
                c.execute("SELECT * FROM all_month WHERE depth>=? and depth<?", (mindep, max))
                y.append(len(c.fetchall()))
                mindep += seg
            conn.close()
            return render_template('pie.html', x=x, y=y, len=len(y))
        elif request.form['point'] == 'line':
            conn = sqlite3.connect('data/test.db')
            c = conn.cursor()
            seg = int(request.form["seg"])
            start = 0
            maxmag = 8
            x = []
            y = []
            while start < maxmag:
                if start + seg < maxmag:
                    max = start + seg
                else:
                    max = maxmag
                c.execute("SELECT * FROM all_month WHERE mag>? and mag<?", (start, max))
                x.append(str(start) + "-" + str(max))
                y.append(len(c.fetchall()))
                start += seg
            conn.close()
            return render_template('line.html', x=x, y=y)
        else:
            return render_template('home.html', result=data, k=len(data), time=timediff)
    else:
        return render_template('home.html', result=data, k=len(data), time=timediff)


def getData():
    conn = sqlite3.connect('data/test.db')
    print("Open database successfully")
    c = conn.cursor()
    starttime = time.time()
    c.execute("select * from all_month")
    data = np.array(c.fetchall())
    endtime = time.time()
    timediff = endtime - starttime
    conn.close()
    return data, timediff


if __name__ == '__main__':
    # application.run(host='0.0.0.0', port=port)
    # application.debug = True
    app.run()
