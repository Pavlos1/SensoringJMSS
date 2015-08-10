# coding: utf-8
import os
import sqlite3 as lite

from flask import Flask
from websocket import handle_websocket

app = Flask(__name__, static_folder='static', static_url_path='')
app.secret_key = os.urandom(24)
app.debug = True
app.port = 80
app.file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "output.txt"), "r")
app.row = []

def get_first_row():
    try:
        filename = os.path.join(file_dir, '../sound_test_data.db')
        con = lite.connect(filename)
        cur = con.cursor()
        cur.execute('select * from data LIMIT 1')
        rows = cur.fetchall()
        if(rows.length):
            app.row = rows[0]
    except lite.Error, e:
        print "Error %s:" % e.args[0]
        return 
        
    finally:
        if con:
            con.close()

def my_app(environ, start_response):  
    path = environ["PATH_INFO"]  
    if path == "/":  
        return app(environ, start_response)  
    elif path == "/websocket":  
        handle_websocket(environ["wsgi.websocket"])   
    else:  
        return app(environ, start_response)  

import views
