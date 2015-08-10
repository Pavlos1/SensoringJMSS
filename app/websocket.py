# coding: utf-8
import json
import os
import app
import time
import sqlite3 as lite

def handle_websocket(ws):
    while True:
        message = ws.receive()
        if message is None:
            break
        else:
            rows = []
            message = json.loads(message)
            init = message['init']
            timestamp = message['time']
            try:
                file_dir = os.path.dirname(__file__)
                filename = os.path.join(file_dir, '../sound_test_data.db')
                con = lite.connect(filename)
                
                cur = con.cursor()
                if(init):
                    cur.execute('select * from data where time > ((select time from data order by time desc limit 1) - ?);', (3600,))
                elif(all (k in message for k in ("startTime", "endTime"))):
                    print "hello"
                    cur.execute('select * from data where time > ? and time < ?;', (message["startTime"], message["endTime"]))
                else:
                    cur.execute('select * from data where time > ?;', (timestamp,))
                rows = cur.fetchall()
                #if(len(rows)):
                if(len(rows) > 0 and rows[0] == app.app.row):
                    ws.send(
                        json.dumps({first: True, time: rows[0][0]})
                    )
                ws.send(
                    json.dumps(rows)
                )
                #cur.execute('SELECT time, sound FROM( SELECT * FROM data ORDER BY time DESC LIMIT 3 ) T1 ORDER BY time')
                
            except lite.Error, e:
                print "Error %s:" % e.args[0]
                return 
                
            finally:
                if con:
                    con.close()
