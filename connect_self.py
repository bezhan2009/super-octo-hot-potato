from main import app
from flask import Flask, jsonify, url_for, request, render_template, redirect, session
import psycopg2


def manually_connect(_db_name, _user, _password):
    if not _db_name:
        _db_name = "postgres"
    elif not _user:
        _user = "postgres"
    elif not _user and not _db_name:
        _user = "postgres"
        _db_name = "postgres"

    db_name = _db_name
    user = _user
    password = _password
    port = "5432"
    host = "127.0.0.1"

    try:
        conn = psycopg2.connect(
            dbname=db_name,
            user=user,
            password=password,
            host=host,
            port=port
        )
    except psycopg2.Error as e:
        print(e)
        return False

    return conn


def redirect_to_connect():
    with app.app_context():
        return render_template("error_connection.html")


def redirect_to_index():
    with app.app_context():
        return redirect("http://127.0.0.1:5000/", code=302)