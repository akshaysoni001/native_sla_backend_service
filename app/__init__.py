#!./bin/python
from flask import Flask, render_template, redirect, url_for, request, send_file, session, flash
from os import path
import logging
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from config import config
from flask_session import Session
from flask_mail import Mail
from werkzeug.security import generate_password_hash, check_password_hash

_author_ = "Akshay Soni"

templates_folder = path.join(path.dirname(path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=templates_folder)
app.config.from_object(config)
app.logger.setLevel(logging.INFO)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "ThisIsMySceretKeys" #"b'\xb1)\xff\x96w\xf4\xa9\x1b\x12\xcd\xe7w\xe8\xe4\xb2\x08\xf9\xda\xce\xdc\xe4\xc2P\x82'"
app.config['SESSION_TYPE'] = 'filesystem'
api = Api(app)
db = SQLAlchemy(app)
mail = Mail(app)
Session(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand)

# Sample Error handler
# @app.errorhandler(status_code)
# def function_name(error):
#     # You can log the error or send an email here
#     return render_template("status_code.html"), status_code
#


def register_error_handlers(app):

    # 400 - Bad Request
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('400.html'), 400

    # 403 - Forbidden
    @app.errorhandler(403)
    def forbidden(e):
        return render_template('403.html'), 403

    # 404 - Page Not Found
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    # 405 - Method Not Allowed
    @app.errorhandler(405)
    def method_not_allowed(e):
        return render_template('405.html'), 405

    # 500 - Internal Server Error
    @app.errorhandler(500)
    def server_error(e):
        return render_template('500.html'), 500
