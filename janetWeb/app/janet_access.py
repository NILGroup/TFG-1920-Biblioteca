#Separating the model information and the model access
#Defines the ways to access or edit the information in the database
import http.client
from app import janet_host, janet_port

#TODO darle formato al mensaje para que sea aceptado por janet, usarl JSONObjet
#si es posible (fijarse en el codigo java de la app del movil)
def sendMessage(m):
    client = http.client.HTTPConnection(janet_host, janet_port)
    client.connect()
    client.request("POST","/api", m)
    response = client.getresponse()
    client.close()
    return response
