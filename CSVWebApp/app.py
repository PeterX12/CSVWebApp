from flask import Flask, render_template, request, redirect, url_for, send_file, flash 
from werkzeug import secure_filename 
from flask_sqlalchemy import SQLAlchemy
import os
import csv
import io
import sqlite3
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

app = Flask(__name__)

db_path = os.path.join(os.path.dirname(__file__), 'database.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['ALLOWED_EXTENSIONS'] = set(['csv'])
app.secret_key = "temp for dev"

db = SQLAlchemy(app)

# If db file does not exist...
file = os.path.isfile("./database.db")
if not file:
    import sqlite3
    from app import db  
    conn = sqlite3.connect('database.db')
    conn.close()
    db.create_all()
    db_path = os.path.join(os.path.dirname(__file__), 'database.db')
    db_uri = 'sqlite:///{}'.format(db_path)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['ALLOWED_EXTENSIONS'] = set(['csv'])
    app.secret_key = "temp for dev"

    db = SQLAlchemy(app)
    
# Classes
class TheFile(db.Model):
    record_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    data = db.Column(db.LargeBinary)

# Functions
def file_check(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# Home Page
@app.route('/')
def index():
    return render_template('index.html')

# Upload Page
@app.route('/upload_page')
def upload_page():
    return render_template('upload.html')

# Uploading the CSV file
@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the file to be uploaded
    selected_file = request.files['file']
    # Check if the file is a CSV file and is valid
    if selected_file and file_check(selected_file.filename):
        filename = secure_filename(selected_file.filename)
        new_file = TheFile(name=filename, data=selected_file.read())
        db.session.add(new_file)
        db.session.commit()
        return redirect(url_for('library'))
    else:
    	return redirect(url_for('upload'))

# Library of the uploaded CSV Files
@app.route('/library')
def library():
	library = TheFile.query.all()
	return render_template('library.html', title="CSV Files", library=library)

# Downloading the individual CSV files
@app.route('/file/<int:record_id>/', methods=['GET'])
def file(record_id):
 	myFiles = db.session.query(TheFile).filter(TheFile.record_id == record_id).first()
 	filename = myFiles.name 
 	return send_file(io.BytesIO(myFiles.data), attachment_filename=myFiles.name, as_attachment=True)

# About Page
@app.route('/about')
def about():
    return render_template('about.html')

# Stats Page
@app.route('/stat')
def stats():
    return render_template('stats.html')
     
if __name__ == '__main__':

	app.run(debug=True)