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


class ActionThirdBook(Action):

    def __init__(self, mongo, wms):
        Action.__init__(self, mongo, wms)

    def accion(self, intent, entities, response, uid, tracker, idioma):
        respuesta = response

        historial = self.mongo.obtener_consulta(uid)

        if 'oclc3' in historial:
            respuesta.update(self.wms.cargarInformacionLibro(historial['oclc3']))
            respuesta['content-type'] = 'single-book'

        return respuesta
