import os
from flask import Flask, redirect, url_for, request, render_template
from pymongo import MongoClient
import requests
import json

app = Flask(__name__)

client = MongoClient(
    os.environ['DB_PORT_27017_TCP_ADDR'],
    27017)
db = client.tododb

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def check():
    data = request.form['value']
    type = request.form['type']

    props = {'type': type, 'externalId': data}

    if(type == 'PH'):
        props['countryCode'] = '+' + data[0]
        props['externalId'] = '+' + data

    r = requests.get('https://ru.account.xiaomi.com/pass/user@externalIdBinded', params = props)
    # return str(r.text)
    # Не смог вытянуть чистый json
    flag = str(r.text)[62]

    addLog(props, flag)

    return flag

def addLog(props, flag):
    data = {
        'type': props['type'],
        'value': props['externalId']
    }
    if(flag == '1'):
        data['reg'] = True
    else:
        data['reg'] = False
    db.logs.insert_one(data)
    return

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

