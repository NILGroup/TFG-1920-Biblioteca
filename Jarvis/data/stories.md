# Saludo
* saludos
    - action_saludos

# Como estas
* como_estas
    - utter_como_estas
    
## Me llamo
* me_llamo{"PER": "Jose Luis"}
    - form_saludos
    - form{"name": "form_saludos"}
    - slot{"persona": "Jose luis"}
    - form{"name": null}
    - slot{"requested_slot": null}

## Saludo me llamo
* saludos
    - action_saludos
* me_llamo{"PER": "Jose Luis"}
    - form_saludos
    - form{"name": "form_saludos"}
    - slot{"persona": "Jose luis"}
    - form{"name": null}
    - slot{"requested_slot": null}
    
## Gracias
* gracias
    - utter_gracias

## Despedida
* despedidas
    - utter_despedida
    
## Quien soy
* quien_soy
    - utter_quien_soy
    
## Insultos
* insultos
    - utter_respuesta_insultos

## Consulta libro autor
* consulta_libro_autor{"PER": "Quevedo"}
    - form_libros
    - form{"name": "form_libros"}
    - slot{"libro": null}
    - slot{"autores": "Quevedo"}
    - form{"name": null}
    - slot{"requested_slot": null}

## Consulta libro autor 2
* consulta_libros_autor{"PER": "Pedro S\u00e1nchez"}
    - form_libros
    - form{"name": "form_libros"}
    - slot{"libro": null}
    - slot{"autores": "Pedro s\u00e1nchez"}
    - form{"name": null}
    - slot{"requested_slot": null}

## Consulta libro autor 3
* consulta_libros_autor{"PER": "Patrick Rothfuss"}
    - form_libros
    - form{"name": "form_libros"}
    - slot{"libro": null}
    - slot{"autores": "Patrick rothfuss"}
    - form{"name": null}
    - slot{"requested_slot": null}

## Consulta libro autor 4
* consulta_libro_autor{"PER": "G\u00f3ngora"}
    - form_libros
    - form{"name": "form_libros"}
    - slot{"libro": null}
    - slot{"autores": "G\u00f3ngora"}
    - form{"name": null}
    - slot{"requested_slot": null}

## Consulta libro titulo autor
* consulta_libro_titulo_autor{"libro": "Don Quijote de la Mancha", "PER": "Miguel de Cervantes"}
    - form_libros
    - form{"name": "form_libros"}
    - slot{"libro": "Don quijote de la mancha"}
    - slot{"autores": "Miguel de cervantes"}
    - form{"name": null}
    - slot{"requested_slot": null}

## Consulta libro tema
* consulta_libro_kw{"libro": "Matem\u00e1tica Discreta y L\u00f3gica"}
    - form_libros
    - form{"name": "form_libros"}
    - slot{"libro": "Matem\u00e1tica discreta y l\u00f3gica"}
    - slot{"autores": null}
    - form{"name": null}
    - slot{"requested_slot": null}

## Consulta libro titulo
* consulta_libros_titulo{"libro": "Narnia"}
    - form_libros
    - form{"name": "form_libros"}
    - slot{"libro": "Narnia"}
    - slot{"autores": null}
    - form{"name": null}
    - slot{"requested_slot": null}

## Consulta libro titulo 2
* consulta_libro_titulo{"libro": "Luces de Bohemia"}
    - form_libros
    - form{"name": "form_libros"}
    - slot{"libro": "Luces de bohemia"}
    - slot{"autores": null}
    - form{"name": null}
    - slot{"requested_slot": null}

## Consulta libro titulo autor
* consulta_libros_titulo_autor{"libro": "Alatriste", "PER": "Arturo P\u00e9rez-Reverte"}
    - form_libros
    - form{"name": "form_libros"}
    - slot{"libro": "Alatriste"}
    - slot{"autores": "Arturo p\u00e9rez-reverte"}
    - form{"name": null}
    - slot{"requested_slot": null}

## Consulta libro tema autor
* consulta_libros_kw_autor{"libro": "Como aprender a programar en 5 minutos", "PER": "Rodolfo Rodr\u00edguez"}
    - form_libros
    - form{"name": "form_libros"}
    - slot{"libro": "Como aprender a programar en 5 minutos"}
    - slot{"autores": "Rodolfo rodr\u00edguez"}
    - form{"name": null}
    - slot{"requested_slot": null}

## Consulta libro tema autor 2
* consulta_libro_kw_autor{"libro": "RSA, de lo mejor lo superior", "autores": "Programador experto"}
    - form_libros
    - form{"name": "form_libros"}
    - slot{"libro": "Rsa, de lo mejor lo superior"}
    - slot{"autores": "Programador experto"}
    - form{"name": null}
    - slot{"requested_slot": null}

## Consulta horario general
* consulta_horario_general{"localizacion": "periodismo"}
    - slot{"localizacion": "periodismo"}
    - action_check_biblio_abierta

## Consulta horario cierre
* consulta_horario_close{"localizacion": "Geologia"}
    - slot{"localizacion": "Geologia"}
    - action_check_biblio_abierta

## Consulta horario apertura
* consulta_horario_open{"localizacion": "Psicologia"}
    - slot{"localizacion": "Psicologia"}
    - action_check_biblio_abierta

## Consulta horario general 2
* consulta_horario_general{"localizacion": "biblioteca zambrano"}
    - slot{"localizacion": "biblioteca zambrano"}
    - action_check_biblio_abierta

## Consulta horario general 3
* consulta_horario_general{"localizacion": "biblioteca de informatica"}
    - slot{"localizacion": "biblioteca de informatica"}
    - action_check_biblio_abierta

## Consulta horario general 4
* consulta_horario_general{"localizacion": "zambrano"}
    - slot{"localizacion": "zambrano"}
    - action_check_biblio_abierta

## Consulta horario general 5
* consulta_horario_general{"MISC": "\u00bfA", "localizaciones": "biblioteca de Psicologia"}
    - action_check_biblio_abierta

## Consulta libros autor
* consulta_libros_autor{"PER": "Federico Garcia Lorca"}
    - form_libros
    - form{"name": "form_libros"}
    - slot{"libro": null}
    - slot{"autores": "Federico Garcia Lorca"}
    - slot{"searchindex": 2}
    - slot{"numberofmorebooksearch": 2}
    - form{"name": null}
    - slot{"requested_slot": null}
* mas_info_primero
    - action_muestra_primero

## Consulta libros autor mas info segundo
* consulta_libros_autor{"PER": "Tolkien"}
    - form_libros
    - form{"name": "form_libros"}
    - slot{"libro": null}
    - slot{"autores": "Tolkien"}
    - slot{"searchindex": 2}
    - slot{"numberofmorebooksearch": 2}
    - form{"name": null}
    - slot{"requested_slot": null}
* mas_info_segundo
    - action_muestra_segundo

## Consulta libro tema mas info tercero
* consulta_libros_kw{"PER": "Pedro Sanchez"}
    - form_libros
    - form{"name": "form_libros"}
    - slot{"libro": null}
    - slot{"autores": "Pedro Sanchez"}
    - slot{"searchindex": 2}
    - slot{"numberofmorebooksearch": 2}
    - form{"name": null}
    - slot{"requested_slot": null}
* mas_info_tercero
    - action_muestra_tercero

## Consulta libro autor mas info todos
* consulta_libros_autor{"PER": "Quevedo"}
    - form_libros
    - form{"name": "form_libros"}
    - slot{"libro": null}
    - slot{"autores": "Quevedo"}
    - slot{"searchindex": 2}
    - slot{"numberofmorebooksearch": 2}
    - form{"name": null}
    - slot{"requested_slot": null}
* mas_info_primero
    - action_muestra_primero
* mas_info_segundo
    - action_muestra_segundo
* mas_info_tercero
    - action_muestra_tercero

## Consulta libro tema muestra mas informacion todos en desorden
* consulta_libros_kw{"MISC": "Derecho Legal Civil"}
    - form_libros
    - form{"name": "form_libros"}
    - slot{"libro": "Derecho Legal Civil"}
    - slot{"autores": null}
    - slot{"searchindex": 2}
    - slot{"numberofmorebooksearch": 2}
    - form{"name": null}
    - slot{"requested_slot": null}
* mas_info_primero
    - action_muestra_primero
* mas_info_tercero
    - action_muestra_tercero
* mas_info_segundo
    - action_muestra_segundo

## Consulta localizacion
* consulta_localizacion{"localizacion": "biblioteca de educacion"}
    - slot{"localizacion": "biblioteca de educacion"}
    - utter_consulta_localizacion

## Consulta localizacion 2
* consulta_telefono{"localizacion": "facultad de informatica"}
    - slot{"localizacion": "facultad de informatica"}
    - utter_consulta_telefono

## Consulta localizacion 3
* consulta_telefono{"localizacion": "facultad de medicina"}
    - slot{"localizacion": "facultad de medicina"}
    - utter_consulta_telefono

## Consulta localizacion 4
* consulta_localizacion{"localizacion": "biblioteca de educacion"}
    - slot{"localizacion": "biblioteca de educacion"}
    - utter_consulta_localizacion

## Consulta telefono vacio
* consulta_telefono_empty
    - action_localizacion_sin_entidad

## Consulta localizacion vacio
* consulta_localizacion_empty
    - action_localizacion_sin_entidad

## Consulta libros tema busca mas
* consulta_libros_kw{"MISC": "Matem\u00e1tica Discreta"}
    - form_libros
    - form{"name": "form_libros"}
    - slot{"libro": "Matem\u00e1tica Discreta"}
    - slot{"autores": null}
    - slot{"searchindex": 2}
    - slot{"numberofmorebooksearch": 2}
    - form{"name": null}
    - slot{"requested_slot": null}
* busca_mas
    - action_busca_mas
    - slot{"searchindex": 4}
* busca_mas
    - action_busca_mas
    - slot{"searchindex": 6}
* busca_mas
    - action_busca_mas
    - slot{"searchindex": 8}

## consulta libros titulo
* consulta_libros_titulo{"MISC": "Harry Potter y el misterio del principe", "libro": "harry potter y el misterio del principe"}
    - form_libros
    - form{"name": "form_libros"}
    - slot{"libro": "Harry Potter y el misterio del principe"}
    - slot{"autores": null}
    - slot{"searchindex": 2}
    - slot{"numberofmorebooksearch": 2}
    - form{"name": null}
    - slot{"requested_slot": null}
    
## No relacionado
* no_relacionado
    - utter_no_relacionado

## Consulta libro vacio
* consulta_libro
    - utter_especifica_libro

## Consulta libros vacio
* consulta_libros
    - utter_especifica_libro

## Consulta libro vacio completa
* consulta_libro
    - utter_especifica_libro
* solo_libro{"libro": "Canción de hielo y fuego"}
    - form_libros
    - form{"name": "form_libros"}
    - slot{"libro": "Canción de hielo y fuego"}
    - slot{"autores": null}
    - form{"name": null}
    - slot{"requested_slot": null}

## Consulta libros vacio completa
* consulta_libros
    - utter_especifica_libro
* solo_libros{"libro": "harry potter y el misterio del principe"}
    - form_libros
    - form{"name": "form_libros"}
    - slot{"libro": "Harry Potter y el misterio del principe"}
    - slot{"autores": null}
    - slot{"searchindex": 2}
    - slot{"numberofmorebooksearch": 2}
    - form{"name": null}
    - slot{"requested_slot": null}

## Consulta libro vacio completa con autor
* consulta_libros
    - utter_especifica_libro
* solo_libro_autor{"libro": "Alatriste", "PER": "Arturo P\u00e9rez-Reverte"}
    - form_libros
    - form{"name": "form_libros"}
    - slot{"libro": "Alatriste"}
    - slot{"autores": "Arturo p\u00e9rez-reverte"}
    - form{"name": null}
    - slot{"requested_slot": null}

## Consulta libro con autor
* solo_libro_autor{"libro": "Alatriste", "PER": "Arturo P\u00e9rez-Reverte"}
    - form_libros
    - form{"name": "form_libros"}
    - slot{"libro": "Alatriste"}
    - slot{"autores": "Arturo p\u00e9rez-reverte"}
    - form{"name": null}
    - slot{"requested_slot": null}

## Consulta solo libro
* solo_libros{"libro": "harry potter y el misterio del principe"}
    - form_libros
    - form{"name": "form_libros"}
    - slot{"libro": "Harry Potter y el misterio del principe"}
    - slot{"autores": null}
    - slot{"searchindex": 2}
    - slot{"numberofmorebooksearch": 2}
    - form{"name": null}
    - slot{"requested_slot": null}

## faq
* faq
    - utter_faq

## edad
* edad
    - utter_edad

## Te quiero
* te_quiero
    - utter_te_quiero

## Chiste
* chiste
    - utter_chiste

## Idiomas
* idiomas
    - utter_idiomas

## Privacidad
* privacidad
    - utter_privacidad