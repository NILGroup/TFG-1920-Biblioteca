NO_RELATED_BOOKS_ES = "Vaya, parece que no hay libros relacionados con esa consulta."
NO_RELATED_BOOKS_EN = "Oh, it seems like there are no books related to that query."
NO_LIBRARY_CALLED_LIKE_THAT_ES = "Vaya, parece que no existe ninguna biblioteca llamada así."
NO_LIBRARY_CALLED_LIKE_THAT_EN = "Oh, it seems like there isn't a library called like that."



def get_custom_response(response, language):
    if (response == "NO_RELATED_BOOKS"):
        if (language == "es"):
            return NO_RELATED_BOOKS_ES
        else:
            return NO_RELATED_BOOKS_EN
    elif (response == "NO_LIBRARY_CALLED_LIKE_THAT"):
        if (language == "es"):
            return NO_LIBRARY_CALLED_LIKE_THAT_ES
        else:
            return NO_LIBRARY_CALLED_LIKE_THAT_EN
    else:
        return NO_RELATED_BOOKS_ES
