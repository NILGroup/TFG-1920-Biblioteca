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

from ActionsController import Action
from Actions.ActionSearchEntity import get_entities_values
from Actions.CustomResponses import get_custom_response


class ActionTitle(Action):

    def __init__(self, mongo, wms):
        Action.__init__(self, mongo, wms)

    def accion(self, intent, entities, response, uid, tracker, idioma):
        respuesta = response

        entities_values = get_entities_values(entities, ['libro'], tracker)
        if entities_values['libro'] is not None:
            respuesta['books'] = self.wms.buscarLibro(entities_values['libro'], None, tracker['searchindex'], 'title')
            if not respuesta['books']:
                del respuesta['books']
                respuesta['content-type'] = 'text'
                respuesta['response'] = get_custom_response("NO_RELATED_BOOKS", idioma)
            else:
                if len(respuesta['books']) == 1:
                    respuesta.update(self.wms.cargarInformacionLibro(respuesta['books'][0]['oclc']))
                    del respuesta['books']
                    respuesta['content-type'] = 'single-book'
                    self.mongo.guardar_consulta(uid, respuesta, 'consulta_libros_titulo')
                    return respuesta

                if intent == 'consulta_libros_titulo':
                    respuesta['content-type'] = 'list-books'
                else:
                    respuesta.update(self.wms.cargarInformacionLibro(respuesta['books'][0]['oclc']))
                    del respuesta['books']
                    respuesta['content-type'] = 'single-book'
                self.mongo.guardar_consulta(uid, respuesta, intent)

        return respuesta
