from flask import render_template, flash, redirect, url_for, request, jsonify
from app import app
from .forms import CreateForm
from .janet_access import *

#Página inicial
@app.route('/', methods=['GET', 'POST'])
def main():
    form = CreateForm()
    flash(form.message.data)

    #Sees if the data from the form is valid
    if form.validate_on_submit():
        #Debug, comprobar que la conexion se realiza
        print(sendMessage(form.message.data))

    return render_template('messages.html',
                           title='Janet',
                           form=form)

@app.route('/process', methods=['POST'])
def process():
    message = request.form['message']

    return sendMessage(message)
