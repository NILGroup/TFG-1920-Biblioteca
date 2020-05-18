from flask import render_template, flash, redirect, url_for, request, jsonify,\
    make_response
from app import app
from .forms import CreateForm
from .janet_access import *
import json

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
    return redirect("http://127.0.0.1:8080", code=307)
