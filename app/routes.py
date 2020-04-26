from flask import Flask, render_template, flash, redirect, url_for, request
from app import app, mysql

@app.route('/')
def main():
    return "Welcome!"