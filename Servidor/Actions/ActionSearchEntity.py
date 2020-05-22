def get_entities_values(entities, look_for, tracker, force_find=True, use_tracker=True, priority_tracker=False):
    result = {}
    #{'autores': None, 'libro': 'El', 'localizacion': 'biblioteca de informatica', 'numberofmorebooksearch': 1, 'persona': 'Miguel', 'requested_slot': None, 'searchindex': 1}

    for ent in look_for:
        if use_tracker and priority_tracker:
            if ent == 'PER':
                result[ent] = tracker['autores']
            else:
                result[ent] = tracker[ent]
        else:
            result[ent] = None    

    for ent in entities:
        if ent['entity'] in look_for and result[ent['entity']] is None:
            result[ent['entity']] = ent['value']
            
    #Busca si no ha encontrado algo y fuerza rellenarlo
    if force_find:
        misc = _find_any(entities)
        for key, value in result.items():
            if value is None:
                if use_tracker and priority_tracker == False:
                    if key == 'PER':
                        result[key] = tracker['autores']
                    else:
                        result[key] = tracker[key]
                elif result[key] is None and misc is not None:
                    result[key] = misc

    return result

#Busca para reemplazar los no encontrados con una entitie MISC
#Si no la encuentra, coge la primera que encuentre
def _find_any(entities):
    if len(entities) == 0:
        return None
    
    for ent in entities:
        if ent['entity'] == 'MISC':
            return ent['value']

    return entities[0]['value']