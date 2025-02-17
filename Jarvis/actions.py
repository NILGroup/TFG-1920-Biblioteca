# -*- coding: utf-8 -*-
"""
Módulo PLN Jarvis - Proyecto Janet
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
from typing import Dict, Text, Any, List, Union

from rasa_sdk import Action
from rasa_sdk import Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction, REQUESTED_SLOT


class ActionSaludos(Action):
    def name(self):
        return 'action_saludos'

    def run(self, dispatcher, tracker, domain):
        persona = tracker.get_slot('persona')
        if persona is not None:
            dispatcher.utter_message(template="utter_saludo_nombre", persona=persona)
            return []
        else:
            dispatcher.utter_message(template="utter_saludo")
            return []

class SaludosForm(FormAction):
    def name(self):
        return "form_saludos"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["persona"]

    def slot_mappings(self):
        return {"persona": [self.from_entity(entity="PER", intent="me_llamo"),
                            self.from_entity(entity="persona", intent="me_llamo")]}

    def validate(self,
                 dispatcher: CollectingDispatcher,
                 tracker: Tracker,
                 domain: Dict[Text, Any]) -> List[Dict]:

        slot_values = self.extract_other_slots(dispatcher, tracker, domain)
        slot_to_fill = tracker.get_slot(REQUESTED_SLOT)

        if slot_to_fill:
            slot_values.update(self.extract_requested_slot(dispatcher, tracker, domain))

        else:
            temp = tracker.get_latest_entity_values('PER')
            aux = None
            for i in temp:
                if i.lower() != "hola":
                    aux = i
            aux2 = next(tracker.get_latest_entity_values('persona'), None)
            loc = next(tracker.get_latest_entity_values('LOC'), None)
            misc = next(tracker.get_latest_entity_values('MISC'), None)
            if aux is None and aux2 is not None:
                return [SlotSet('persona', aux2.title())]
            elif aux is not None and aux is not "Hola":
                return [SlotSet('persona', aux.title())]
            elif loc is not None:
                return [SlotSet('persona', loc)]
            elif misc is not None:
                return [SlotSet('persona', misc)]
            else:
                dispatcher.utter_message(template="utter_tell_me_name")
                return []

        return [SlotSet(slot, value) for slot, value in slot_values.items()]

    def submit(self,
               dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any]) -> List[Dict]:
        persona = tracker.get_slot('persona')
        if persona is not None:
            dispatcher.utter_message(template="utter_saludo_nombre",persona=persona)
            return [SlotSet('persona', persona)]
        else:
            dispatcher.utter_message(template="utter_saludo")
            return []

class BuscarLibroForm(FormAction):
    def name(self):
        return "form_libros"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return []

    def slot_mapping(self):
        return {"libro": [self.from_entity(entity="libro"),
                          self.from_entity(entity="MISC")],
                "autores":  [self.from_entity(entity="PER"),
                          self.from_entity(entity="autores")]
                }

    def validate(self,
                 dispatcher: CollectingDispatcher,
                 tracker: Tracker,
                 domain: Dict[Text, Any]) -> List[Dict]:
        temp = {}
        intent = tracker.latest_message['intent'].get('name')
        MISC = next(tracker.get_latest_entity_values('MISC'), None)
        libro = next(tracker.get_latest_entity_values('libro'), None)
        ORG = next(tracker.get_latest_entity_values('ORG'), None)
        loc = next(tracker.get_latest_entity_values('LOC'), None)
        PER = next(tracker.get_latest_entity_values('PER'), None)
        temp['libro'] = None
        temp['autores'] = None

        if intent == 'consulta_libros_kw' or intent == 'consulta_libro_kw' or intent == 'solo_libro' or \
                intent == 'consulta_libros_titulo_autor' or intent == 'consulta_libro_titulo_autor' or \
                intent == 'consulta_libros_titulo' or intent == 'consulta_libro_titulo' or \
                intent == 'consulta_libros_kw_autor' or intent == 'consulta_libro_kw_autor' or \
                intent == 'solo_libros' or intent == 'solo_libro_autor':
            if (MISC is not None and libro is None) or (MISC is not None and libro is not None and len(libro) < len(MISC)):
                temp['libro'] = next(tracker.get_latest_entity_values('MISC'), None)
            elif libro is not None:
                temp['libro'] = libro.capitalize()
            elif loc is not None:
                temp['libro'] = loc
            elif PER is not None:
                temp['libro'] = PER
            elif ORG is not None:
                temp['libro'] = ORG

        if intent == 'consulta_libros_autor' or intent == 'consulta_libro_autor' or intent == 'solo_libro' or \
                intent == 'consulta_libros_autor' or intent == 'consulta_libro_autor' or \
                intent == 'consulta_libros_titulo_autor' or intent == 'consulta_libro_titulo_autor' or \
                intent == 'consulta_libros_kw_autor' or intent == 'consulta_libro_kw_autor' or \
                intent == 'solo_libros' or intent == 'solo_libro_autor':
            if PER is not None:
                if temp['libro'] is not None and PER.lower() == temp['libro'].lower():
                    autores = tracker.get_latest_entity_values('PER')
                    aux = None
                    for i in autores:
                        if i.lower() != temp['libro'].lower():
                            aux = i
                    temp['autores'] = aux
                else:
                    temp['autores'] = PER

        return [SlotSet('libro', temp['libro']), SlotSet('autores', temp['autores'])]


    def submit(self,
               dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any]) -> List[Dict]:
        libro = tracker.get_slot('libro')
        autores = tracker.get_slot('autores')
        intent = tracker.latest_message['intent'].get('name')
        numIndexes = 0
        numberofmorebooksearch = 0

        if intent == "consulta_libros_kw":
            if libro is not None:
                dispatcher.utter_message(template="utter_libros_kw", libro=libro)
                numIndexes = 2
                numberofmorebooksearch = 2
            else:
                dispatcher.utter_message(template="utter_especifica_libro")
        elif intent == "consulta_libros_autor":
            if autores is not None:
                dispatcher.utter_message(template="utter_libros_autor",autores=autores)
                numIndexes = 2
                numberofmorebooksearch = 2
            else:
                dispatcher.utter_message(template="utter_especifica_libro")
        elif intent == "consulta_libro_titulo_autor" or intent == 'solo_libro_autor':
            if libro is not None and autores is not None:
                dispatcher.utter_message(template="utter_libro_titulo_autor", libro=libro, autores=autores)
                numIndexes = 1
                numberofmorebooksearch = 1
            else:
                dispatcher.utter_message(template="utter_especifica_libro")
        elif intent == "consulta_libro_kw":
            if libro is not None:
                dispatcher.utter_message(template="utter_libro_kw", libro=libro)
                numIndexes = 1
                numberofmorebooksearch = 1
            else:
                dispatcher.utter_message(template="utter_especifica_libro")
        elif intent == "consulta_libros_titulo" or intent == "solo_libros":
            if libro is not None:
                dispatcher.utter_message(template="utter_libros_titulo", libro=libro)
                numIndexes = 2
                numberofmorebooksearch = 2
            else:
                dispatcher.utter_message(template="utter_especifica_libro")
        elif intent == "consulta_libro_titulo" or intent == "solo_libro":
            if libro is not None:
                dispatcher.utter_message(template="utter_libro_titulo", libro=libro)
                numIndexes = 1
                numberofmorebooksearch = 1
            else:
                dispatcher.utter_message(template="utter_especifica_libro")
        elif intent == "consulta_libro_autor":
            if autores is not None:
                dispatcher.utter_message(template="utter_libro_autor", autores=autores)
                numIndexes = 1
                numberofmorebooksearch = 1
            else:
                dispatcher.utter_message(template="utter_especifica_libro")
        elif intent == "consulta_libros_titulo_autor":
            if libro is not None and autores is not None:
                dispatcher.utter_message(template="utter_libros_titulo_autor", libro=libro, autores=autores)
                numIndexes = 2
                numberofmorebooksearch = 2
            else:
                dispatcher.utter_message(template="utter_especifica_libro")
        elif intent == "consulta_libros_kw_autor":
            if libro is not None and autores is not None:
                dispatcher.utter_message(template="utter_libros_kw_autor", libro=libro, autores=autores)
                numIndexes = 2
                numberofmorebooksearch = 2
            else:
                dispatcher.utter_message(template="utter_especifica_libro")
        elif intent == "consulta_libro_kw_autor":
            if libro is not None and autores is not None:
                dispatcher.utter_message(template="utter_libro_kw_autor", libro=libro, autores=autores)
                numIndexes = 1
                numberofmorebooksearch = 1
            else:
                dispatcher.utter_message(template="utter_especifica_libro")
        return [SlotSet('searchindex', numIndexes), SlotSet('numberofmorebooksearch', numberofmorebooksearch)]

class ActionBuscaMas(Action):
    def name(self):
        return 'action_busca_mas'

    def run(self, dispatcher, tracker, domain):
        libros = tracker.get_slot('libro')
        autores = tracker.get_slot('autores')
        numberofmorebooksearch = tracker.get_slot('numberofmorebooksearch')
        numIndexes = tracker.get_slot('searchindex')

        if libros is not None:
            dispatcher.utter_message(template="utter_muestra_mas")
        elif autores is not None:
            dispatcher.utter_message(template="utter_muestra_mas")
        else:
            dispatcher.utter_message(template="utter_indica_algo")
            return [SlotSet('searchindex', 0), SlotSet('numberofmorebooksearch', 0)]
        if numberofmorebooksearch == 1:
            return [SlotSet('searchindex', numIndexes + 2)]
        else:
            return [SlotSet('searchindex', numIndexes + 3)]

class ActionMuestraPrimero(Action):
    def name(self):
        return 'action_muestra_primero'

    def run(self, dispatcher, tracker, domain):
        libros = tracker.get_slot('libro')
        autores = tracker.get_slot('autores')
        if libros is not None:
            dispatcher.utter_message(template="utter_primero_list",libros=libros)
        elif autores is not None:
            dispatcher.utter_message(template="utter_primero_list",autores=autores)
        else:
            dispatcher.utter_message(template="utter_indica_algo")
        return []

class ActionMuestraSegundo(Action):
    def name(self):
        return 'action_muestra_segundo'

    def run(self, dispatcher, tracker, domain):
        libros = tracker.get_slot('libro')
        autores = tracker.get_slot('autores')
        numberofmorebooksearch = tracker.get_slot('numberofmorebooksearch')
        if numberofmorebooksearch is None or numberofmorebooksearch == 1:
            dispatcher.utter_message(template="utter_solo_un_libro")
        elif libros is not None:
            dispatcher.utter_message(template="utter_segundo_list", libros=libros)
        elif autores is not None:
            dispatcher.utter_message(template="utter_segundo_list", autores=autores)
        else:
            dispatcher.utter_message(template="utter_indica_algo")
        return []

class ActionMuestraTercero(Action):
    def name(self):
        return 'action_muestra_tercero'

    def run(self, dispatcher, tracker, domain):
        libros = tracker.get_slot('libro')
        autores = tracker.get_slot('autores')
        numberofmorebooksearch = tracker.get_slot('numberofmorebooksearch')
        if numberofmorebooksearch is None or numberofmorebooksearch == 1:
            dispatcher.utter_message(template="utter_solo_un_libro")
        elif libros is not None:
            dispatcher.utter_message(template="utter_tercero_list", libros=libros)
        elif autores is not None:
            dispatcher.utter_message(template="utter_tercero_list", autores=autores)
        else:
            dispatcher.utter_message(template="utter_indica_algo")
        return []

class ActionHayLocalizacion(Action):
    def name(self):
        return 'action_localizacion_sin_entidad'

    def run(self, dispatcher, tracker, domain):
        localizacion = tracker.get_slot('localizacion')
        intent = tracker.latest_message['intent'].get('name')
        if localizacion is not None:
            if intent == 'consulta_localizacion_empty':
                dispatcher.utter_message(template="utter_consulta_localizacion")
            elif intent == 'consulta_telefono_empty':
                dispatcher.utter_message(template="utter_consulta_telefono")
            elif intent == 'consulta_email_empty':
                dispatcher.utter_message(template="utter_consulta_email")
        else:
            dispatcher.utter_message(template="utter_indica_biblioteca")
        return []


class ActionComprobarApertura(Action):
    def name(self):
        return 'action_check_biblio_abierta'

    def tratarEntrada(self, entrada):
        entrada = entrada.replace('biblioteca de ', '')
        entrada = entrada.replace('facultad de ', '')
        entrada = entrada.replace('Biblioteca de ', '')
        entrada = entrada.replace('Facultad de ', '')
        entrada = entrada.replace('Biblioteca De ', '')
        entrada = entrada.replace('Facultad De ', '')
        entrada = entrada.replace('BIBLIOTECA DE ', '')
        entrada = entrada.replace('FACULTAD DE ', '')
        entrada = entrada.replace('biblioteca ', '')
        entrada = entrada.replace('facultad ', '')
        entrada = entrada.replace('Biblioteca ', '')
        entrada = entrada.replace('Facultad ', '')
        entrada = entrada.replace('Biblioteca ', '')
        entrada = entrada.replace('Facultad ', '')
        entrada = entrada.replace('BIBLIOTECA ', '')
        entrada = entrada.replace('FACULTAD ', '')

        return entrada

    def run(self, dispatcher, tracker, domain):
        localizacion = tracker.get_slot('localizacion')
        if localizacion is not None:
            from pymongo import MongoClient
            from datetime import datetime
            client = MongoClient('mongodb://localhost:27017')
            db = client.janet
            collection = db.localizaciones

            cursor = collection.find({"$text": {'$search': self.tratarEntrada(localizacion)}},
                                     {'_id': False, 'kw': False, 'score':
                                         {'$meta': "textScore"}}).sort([('score', {'$meta': "textScore"})]).limit(1)
            biblioteca = None
            for doc in cursor:
                biblioteca = doc
            client.close()

            if biblioteca is None:
                dispatcher.utter_message(template="utter_indica_biblioteca")
            else:
                intent = tracker.latest_message['intent'].get('name')
                hora_actual = datetime.now().strftime('%H:%M')
                hora_actual = datetime.strptime(hora_actual, '%H:%M')
                hora_apertura = datetime.strptime(biblioteca["open_hour"], '%H:%M')
                hora_cierre = datetime.strptime(biblioteca["close_hour"], '%H:%M')

                if intent == "consulta_horario_general":
                    if biblioteca["days_opened"] == 4:
                        dispatcher.utter_message("El horario de la " + biblioteca["name"] + " es de "
                                                "lunes a viernes de " + hora_apertura.strftime('%H:%M') + " a " +
                                                 hora_cierre.strftime('%H:%M') + ".")
                    else:
                        dispatcher.utter_message("El horario de la " + biblioteca["name"] + " es de "
                                                 "lunes a domingo de " + hora_apertura.strftime('%H:%M') + " a " +
                                                 hora_cierre.strftime('%H:%M') + ".")
                else:
                    if biblioteca["days_opened"] < datetime.today().weekday():
                        dispatcher.utter_message(template="utter_consulta_horario_cerrado")
                    elif hora_actual < hora_apertura or hora_actual > hora_cierre:
                        dispatcher.utter_message(template="utter_consulta_horario_cerrado")
                    else:
                        dispatcher.utter_message(template="utter_consulta_horario_abierto")
        else:
            dispatcher.utter_message(template="utter_indica_biblioteca")
        return []
