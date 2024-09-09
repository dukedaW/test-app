from flask import Flask, render_template, jsonify, Blueprint, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///task2.db"
app.config['SECRET_KEY'] = 'key'
db = SQLAlchemy(app)
