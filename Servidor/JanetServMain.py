# -*- coding: utf-8 -*-
"""
Servidor de TFG - Proyecto Janet
Versión 1.0

MIT License

Copyright (c) 2019 Mauricio Abbati Loureiro - Jose Luis Moreno Varillas

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial
portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN
NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from bottle import request, route, run, response, static_file, error, abort
import urllib
import JanetServController
import json
from rasa.core.agent import Agent


class JanetService:
    def __init__(self):
        print("Iniciando módulos.".encode('utf-8'), flush=True)
        self.controlador = JanetServController.JanetServController()
        print("Preparado.".encode('utf-8'), flush=True)

        @route('/api', method='POST')
        def do_listen():
            """
            Dirección en la que se reciben las llamadas de los clientes.
            """
            response.content_type = 'application/json'
            response.status = 200

            post_data = {}
            post_data["type"] = request.POST.type
            post_data["content"] = request.POST.content
            post_data["user_id"] = request.POST.user_id
            print("Usuario conectado por POST: ".encode('utf-8'), post_data["user_id"].encode('utf-8'), flush=True)
            print("--- Mensaje: : ".encode('utf-8'), post_data["content"].encode('utf-8'), flush=True)
            try:
                """ Teniendo todos los datos, se pasan al controlador para decidir que se hace con ellos """
                respuesta = self.controlador.procesarDatos_POST(post_data)
                return respuesta
            except urllib.error.HTTPError as e:
                if e.code == 400:
                    abort(400, e.reason)
                else:
                    raise


        @route('/', method='GET')
        def do_test():
            HTML = '''<img src="static/icon.png" alt="Logo" width="500" height="500"> <br> <h1> No deberias estar aqui! </h1> <p> Esta direccion es de prueba, conectate con un cliente.</p>'''
            return HTML

        @route('/static/<filepath:path>')
        def server_static(filepath):
            return static_file(filepath, root='./')

        @error(400)
        def custom400(error):
            '''Cuando ocurre un error, bottle no lo convierte en JSON automáticamente,
            así que lo hacemos nosotros. Primero ponemos el `content_type`, y luego
            hacemos el `json.dumps` del diccionario. En el error 400, decimos que ha
            habido un error y en los detalles ponemos la explicación para que el usuario
            sepa qué ha hecho mal.'''
            response.content_type = 'application/json'
            print("ERROR 400: ".encode('utf-8'), error.body.encode('utf-8'), flush=True)
            return json.dumps({
                'errorno': 400,
                'errorMessage': error.body
            })

        @error(404)
        def custom404(error):
            '''El error 404 no necesita demasiada información.'''
            response.content_type = 'application/json'
            print("ERROR 404: ".encode('utf-8'), error.body.encode('utf-8'), flush=True)
            return json.dumps({
                'errorno': 404,
                'errorMessage': 'No existe el recurso solicitado.'
            })

        @error(500)
        def custom500(error):
            '''En el caso del error 500, no le damos información al usuario porque son
            detalles de nuestro servidor y puede ser un fallo de seguridad. Estos
            errores ocurren cuando nuestro código python ha fallado, por lo que habrá
            que mirar la salida de error del programa para verlos.'''
            response.content_type = 'application/json'
            print("ERROR 500: ".encode('utf-8'), str(error.exception).encode('utf-8'), flush=True)
            return json.dumps({
                'errorno': 500,
                'errorMessage': 'Ha habido un problema imprevisto.',
            })


if __name__ == '__main__':
    JanetService()
    run(host='0.0.0.0', port=8080, reloader=True, interval=3600)
