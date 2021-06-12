from flask import Flask
import os
import sqlite3
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

file = os.path.isfile("./database.db")
if file:
    db_path = os.path.join(os.path.dirname(__file__), 'database.db')
    db_uri = 'sqlite:///{}'.format(db_path)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['ALLOWED_EXTENSIONS'] = set(['csv'])
    app.secret_key = ";fd;jf;ldsjf;lsdjgdfajgfajgp 'ierajgweug'iagjr'u"
    db = SQLAlchemy(app)
else:
    conn = sqlite3.connect('database.db')
    conn.close()
    from app import db 
    db.create_all()
    

@app.route('/')
def index():
    return 'Hello, World!'

if __name__ == "__main__":
    app.run(debug=True)