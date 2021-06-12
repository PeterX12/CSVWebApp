from flask import Flask, render_template, request, redirect, url_for, send_file, flash 
from werkzeug import secure_filename 
from flask_sqlalchemy import SQLAlchemy
import os
import csv
import io
import sqlite3
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

file = os.path.isfile("./database.db")
# If db file exists...
if file:
    db_path = os.path.join(os.path.dirname(__file__), 'database.db')
    db_uri = 'sqlite:///{}'.format(db_path)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['ALLOWED_EXTENSIONS'] = set(['csv'])
    app.secret_key = ";fd;jf;ldsjf;lsdjgdfajgfajgp 'ierajgweug'iagjr'u"
    db = SQLAlchemy(app)
# If db file does not exist...
else:
    conn = sqlite3.connect('database.db')
    conn.close()
    from app import db 
    db.create_all()
    
# Classes
class TheFile(db.Model):
    record_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    data = db.Column(db.LargeBinary)

# Functions
def file_check(file):
    return '.' in file and \
        file.rsplit('.',1)[1] in app.config['ALLOWED_EXTENSIONS'] 

# Home Page
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)