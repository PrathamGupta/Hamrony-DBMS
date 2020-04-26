from flask import Flask, render_template, flash, redirect, url_for, request
from flask_mysqldb import MySQL

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_USER'] = 'pratham'
app.config['MYSQL_PASSWORD'] = 'Pratham@123'
app.config['MYSQL_DB'] = 'dbms'
app.config['MYSQL_HOST'] = 'localhost'
mysql.init_app(app)


from app import routes

