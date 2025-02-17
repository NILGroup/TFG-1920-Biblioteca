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

from urllib import request, parse, error
from socket import timeout
from langdetect import detect
import json
from rasa.core.agent import Agent
from rasa.core.channels import UserMessage
from rasa.core.tracker_store import MongoTrackerStore
from rasa.core.domain import Domain
from rasa.utils.endpoints import EndpointConfig
import asyncio


class JanetServJarvis():

    """"Carga la URL de la localización de Jarvis del fichero 'parameters.conf'"""
    def __init__(self):
        """ Se generan los trackers y se asocian a agentes ambos para ingles y espanol """
        with open(r'parameters.conf', encoding="utf-8") as f:
            datos = json.load(f)
        self.track_store = MongoTrackerStore(
            domain=Domain.load("../Jarvis/domain.yml"),           
            host=datos['url'],
            db=datos['db'],
            username=datos['username'],
            password=datos['password']
        )
        self.track_store_en = MongoTrackerStore(
            domain=Domain.load("../Jarvis/domain_en.yml"),           
            host=datos['url'],
            db=datos['db'],
            username=datos['username'],
            password=datos['password']
        )
        action_endpoint = EndpointConfig(url="http://localhost:5055/webhook")
        self.agent = Agent.load('../Jarvis/models/latest.tar.gz',
            action_endpoint=action_endpoint,
            tracker_store=self.track_store,
        )
        self.agent_en = Agent.load('../Jarvis/models/latest_en.tar.gz',
            action_endpoint=action_endpoint,
            tracker_store=self.track_store_en,
        )

    async def handle_message_async(self, data):
        """ Dado un mensaje, estima el idioma en el que esta y lo analiza con su correspondiente tracker,
        calculando intenciones, el estado del tracker y la respuesta  """
        mensaje_de_usuario = data['message']
        idioma = detect(mensaje_de_usuario)
        if idioma == 'es':
                print('Detectado español'.encode('utf-8'), flush=True)
                resp = await self.agent.handle_message(mensaje_de_usuario, sender_id=data['sender'])
                tracker = self.track_store.get_or_create_tracker(data['sender'])
                output = await self.agent.parse_message_using_nlu_interpreter(mensaje_de_usuario, tracker)
        elif idioma == 'en':
                print('Detectado inglés'.encode('utf-8'), flush=True)
                resp = await self.agent_en.handle_message(mensaje_de_usuario, sender_id=data['sender'])
                tracker = self.track_store_en.get_or_create_tracker(data['sender'])
                output = await self.agent_en.parse_message_using_nlu_interpreter(mensaje_de_usuario, tracker)
        else: # predeterminado en español
                fraseLog = 'Se ha detectado que el idioma era ' + idioma + ' pero se ha respondido en español'
                print(fraseLog.encode('utf-8'), flush=True)
                idioma = 'es'
                resp = await self.agent.handle_message(mensaje_de_usuario, sender_id=data['sender'])
                tracker = self.track_store.get_or_create_tracker(data['sender'])
                output = await self.agent.parse_message_using_nlu_interpreter(mensaje_de_usuario, tracker)
        return resp, output, tracker, idioma
    
    def consultar(self, pregunta, id):
        """ Dado un mensaje y un id de usuario estima la respuesta teniendo en cuenta los ultimos mensajes de dicho usuario """
        contenido = pregunta
        contenido = contenido[0].lower() + contenido[1:]
        data = {'sender': id, 'message': contenido}

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            resp, output, tracker, idioma = loop.run_until_complete(self.handle_message_async(data))
        except error.URLError as e:
            if isinstance(e.reason, timeout):
                msg = "Janet se encuentra en mantenimiento en estos momentos. " \
                          "Inténtelo de nuevo más tarde"
                raise error.HTTPError(self._url, 400, msg, None, None)
            if hasattr(e, 'code') and e.code == 400:
                msg = "Janet se encuentra en mantenimiento en estos momentos. " \
                          "Inténtelo de nuevo más tarde"
                raise error.HTTPError(self._url, 400, msg, None, None)
            else:
                raise error.HTTPError(self._url, 500, e.reason, None, None)
        finally:
            loop.close()

        return resp, output, tracker, idioma

    def restart(self, id):
        data = {'user_id': id, 'content': '/restart'}

        req = request.Request(self._url, data=parse.urlencode(data).encode())
        request.urlopen(req, timeout=10)
