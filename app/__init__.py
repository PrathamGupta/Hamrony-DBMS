from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'pratham'
app.config['MYSQL_DATBASE_PASSWORD'] = 'Pratham@123'
app.config['MYSQL_DATABASE_DB'] = 'dbms'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


from app import routes