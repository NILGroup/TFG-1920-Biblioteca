def get_entities_values(entities, look_for, force_find=True):
    result = {}
    for ent in look_for:
        result[ent] = None

    for ent in entities:
        if ent['entity'] in look_for:
            result[ent['entity']] = ent['value']

    #Busca si no ha encontrado algo y fuerza rellenarlo
    if force_find:
        misc = _find_any(entities)
        if misc is not None:
            for key, value in result.items():
                if value is None:
                    result[key] = misc

    return result

#Busca para reemplazar los no encontrados con una entitie MISC
#Si no la encuentra, coge la primera que encuentre
def _find_any(entities):
    for ent in entities:
        if ent['entity'] == 'MISC':
            return ent['value']
    return entities[0]['value']