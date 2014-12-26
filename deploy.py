from flask import Flask
from flask import render_template, request, session, g, redirect, url_for, abort, flash
import os
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime


# Create application
app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    SQLALCHEMY_DATABASE_URI=os.environ['DATABASE_URL'],
    SECRET_KEY='2g2JXhqfutWCzRBAnuUpTRVNoneadventureatatimebaconandburrata',
    USERNAME='snowman',
    PASSWORD='pumpkin',
    PC_NAME=['peter', 'moop', 'peter cottle', 'peter michael cottle'],
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
