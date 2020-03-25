from flask import render_template, flash, redirect, url_for, request, jsonify,\
    make_response
from app import app
from .forms import CreateForm
from .janet_access import *

#Página inicial
@app.route('/', methods=['GET', 'POST'])
def main():
    privacy = request.cookies.get('janetWeb-privacy')
    if privacy is not None and privacy == 'true':
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
    privacy = request.cookies.get('janetWeb-privacy')
    if privacy is not None and privacy == 'true':
        return redirect(url_for('main'))
    resp = make_response(render_template('privacy.html', title='Janet'))
    return resp

@app.route('/process', methods=['POST'])
def process():
    message = request.form['message']

    return sendMessage(message)

@app.route('/processAudio', methods=['POST'])
def processAudio():
    audioWAV = request.files['audio'].read()

    spokenText = speechToText(audioWAV)

    return spokenText
