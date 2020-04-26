from flask import Flask, render_template, flash, redirect, url_for, request
from app import app, mysql

@app.route('/')
def main():
    return "Welcome!"

@app.route('/meet')
def meet():
    curr=mysql.connection.cursor()
    curr.execute("select * from users")
    data = curr.fetchall()
    return render_template("meet.html", info=data)
