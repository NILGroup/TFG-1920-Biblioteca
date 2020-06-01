from flask import render_template, flash, redirect, url_for, request, jsonify,\
    make_response
import requests
from app import app
from .forms import CreateForm
from .janet_access import *
import json
import unicodedata

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

#Página inicial
@app.route('/', methods=['GET', 'POST'])
def main():
    cookie = request.cookies.get('janetWeb')
    if cookie is not None and json.loads(cookie)['accept_policy'] == 'true':
        form = CreateForm()
        flash(form.message.data)
        resp = make_response(render_template('messages.html',
                            title='Janet',
                            form=form))
        return resp
    else:
        return redirect(url_for('privacy'))

@app.route('/privacy', methods=['GET'])
def privacy():
    cookie = request.cookies.get('janetWeb')
    if cookie is not None and json.loads(cookie)['accept_policy'] == 'true':
        return redirect(url_for('main'))
    resp = make_response(render_template('privacy.html', title='Janet'))
    return resp

@app.route('/process', methods=['POST'])
def process():
    message = request.form['message']
    cookie = request.cookies.get('janetWeb')
    if cookie is None:
        sessionid = "-1"
    else:
        sessionid = json.loads(cookie)['id']
    return sendMessage(message, sessionid)

@app.route('/processAudio', methods=['POST'])
def processAudio():
    audioWAV = request.files['audio'].read()

    spokenText = speechToText(audioWAV)

    return spokenText

@app.route('/api', methods=['POST', 'GET'])
def redirectToJanet():
    print('Recibida conexion desde app movil:', request.get_data(as_text=True).encode('utf-8'))
    client = http.client.HTTPConnection(janet_host, janet_port)
    client.connect()
    json_data = json.dumps('&'+remove_accents(request.get_data(as_text=True))+'&')
    client.request("POST","/api",json_data,{'Content-type':'application/json'})
    response = client.getresponse()
    respStr = response.read().decode('utf-8')
    print('Respuesta:', respStr.encode('utf-8'))
    client.close()
    return respStr
