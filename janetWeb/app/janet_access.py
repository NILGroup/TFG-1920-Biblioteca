#Separating the model information and the model access
#Defines the ways to access or edit the information in the database
import http.client
import speech_recognition as sr
from app import janet_host, janet_port
import json
import io

#TODO darle formato al mensaje para que sea aceptado por janet, usarl JSONObjet
#si es posible (fijarse en el codigo java de la app del movil)
def sendMessage(m, sessionid):
	client = http.client.HTTPConnection(janet_host, janet_port)
	client.connect()
	headers = {'Content-type': 'application/json'}
	query = '&content=' + m + '&user_id=' + sessionid + '&type=query&' #Si os preguntais por que & al principio y al final pues yo que se, pero asi funciona y si no el servidor recibe campos en blanco y pone " Detras de otros
	json_data = json.dumps(query)
	client.request("POST","/api", json_data, headers)
	response = client.getresponse()
	#f.write("data:" + json_data + '\n')
	#f.write("response: " + response.read().decode('utf-8') + '\n')
	responseString = response.read().decode('utf-8')
	client.close()
	return responseString

def speechToText(audioWAV):
	r = sr.Recognizer()

	#Creates a file in memory to be read by te speechToText
	file_obj = io.BytesIO()  # create file-object
	file_obj.write(audioWAV) # write in file-object
	file_obj.seek(0)

	with sr.AudioFile(file_obj) as source:
		audio = r.record(source)

	try:
		text = r.recognize_google(audio, language="es-ES")
		return text

	except Exception as e:
		print("Error on SpeechToText: " + str(e))
		return ''
	
