from flask import Flask, request, render_template
import sqlite3
import subprocess
import os
import yaml
import requests
import random
import pickle
import hashlib

app = Flask(__name__)

# Hardcoded Secret
SECRET_KEY = "123456789"

# Hardcoded Password
DB_PASSWORD = "admin123"

@app.route("/")
def home():
    return render_template("index.html")

####################################################
# SQL Injection
####################################################
@app.route("/login")
def login():

    username = request.args.get("username")
    password = request.args.get("password")

    conn = sqlite3.connect("demo.db")

    cursor = conn.cursor()

    query = "SELECT * FROM users WHERE username=? AND password=?"

    cursor.execute(query, (username, password))

    return "Logged"

####################################################
# Command Injection
####################################################
@app.route("/ping")
def ping():

    ip = request.args.get("ip")

    output = subprocess.check_output(
        "ping -c 1 " + ip,
        shell=True
    )

    return output

####################################################
# Path Traversal
####################################################
@app.route("/read")
def read():

    filename = request.args.get("file")

    with open(filename) as f:
        return f.read()

####################################################
# SSRF
####################################################
@app.route("/fetch")
def fetch():

    url = request.args.get("url")

    r = requests.get(url)

    return r.text

####################################################
# Weak Random
####################################################
@app.route("/token")
def token():

    token = random.randint(100000,999999)

    return str(token)

####################################################
# Weak Crypto
####################################################
@app.route("/hash")
def hash():

    text = request.args.get("text")

    return hashlib.md5(text.encode()).hexdigest()

####################################################
# Eval Injection
####################################################
@app.route("/calc")
def calc():

    data = request.args.get("exp")

    return str(eval(data))

####################################################
# YAML Unsafe Load
####################################################
@app.route("/yaml",methods=["POST"])
def load_yaml():

    return str(yaml.load(request.data, Loader=yaml.Loader))

####################################################
# Pickle
####################################################
@app.route("/pickle",methods=["POST"])
def load_pickle():

    return str(pickle.loads(request.data))

if __name__ == "__main__":
    app.run(debug=True)
