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


class ActionMoreBooks(Action):

    def __init__(self, mongo, wms):
        Action.__init__(self, mongo, wms)

    def accion(self, intent, entities, response, uid, tracker, idioma):
        respuesta = response
        libro = None
        historial = self.mongo.obtener_consulta(uid)
        intentant = historial['intent']
        entities_values = get_entities_values(entities, ['PER', 'libro'], tracker)
        if entities_values['PER'] is not None and entities_values['libro'] is not None:
            libro = self.wms.buscarLibro(entities_values['libro'], entities_values['PER'],
                                                        tracker['searchindex'], self._acortarkwconsulta(intentant))
        elif entities_values['libro'] is not None:
            libro = self.wms.buscarLibro(entities_values['libro'], None,
                                                        tracker['searchindex'], self._acortarkwconsulta(intentant))
        elif entities_values['PER'] is not None:
            libro = self.wms.buscarLibro(None, entities_values['PER'],
                                                        tracker['searchindex'], self._acortarkwconsulta(intentant))
        
        if libro is None:
            respuesta['content-type'] = 'text'
            respuesta['response'] = get_custom_response("NO_RELATED_BOOKS", idioma)

        else:
            if len(libro) == 1:
                    respuesta.update(self.wms.cargarInformacionLibro(libro[0]['oclc']))
                    del libro
                    respuesta['content-type'] = 'single-book'
                    self.mongo.guardar_consulta(uid, respuesta, intentant.replace('libros', 'libro'))
                    return respuesta
            elif intentant == 'consulta_libros_kw' or intentant == 'consulta_libros_titulo' or \
                    intentant == 'consulta_libros_autor' or intentant == 'consulta_libros_titulo_autor' \
                    or intentant == 'consulta_libros_kw_autor':
                respuesta['content-type'] = 'list-books'
            else:
                respuesta.update(self.wms.cargarInformacionLibro(libro[0]['oclc']))
                del libro
                respuesta['content-type'] = 'single-book'
            self.mongo.guardar_consulta(uid, respuesta, intentant)

        return respuesta

    def _acortarkwconsulta(self, intent):
        if intent == 'consulta_libros_kw' or intent == 'consulta_libro_kw':
            return 'kw'
        elif intent == 'consulta_libros_titulo' or intent == 'consulta_libro_titulo':
            return 'title'
        elif intent == 'consulta_libros_autor' or intent == 'consulta_libro_autor':
            return 'author'
        elif intent == 'consulta_libros_titulo_autor' or intent == 'consulta_libro_titulo_autor':
            return 'title_author'
        elif intent == 'consulta_libros_kw_autor' or intent == 'consulta_libro_kw_autor':
            return 'kw_autor'
        else:
            return None
