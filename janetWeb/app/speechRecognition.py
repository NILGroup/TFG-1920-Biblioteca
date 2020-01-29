#sudo pip3 install SpeechRecognition
#sudo pip3 install PyAudio
#Personalmente me da problemas al instalar PyAudio asique hice todo esto (no se que funcionó)
	# sudo apt-get install portaudio19-dev python3-pyaudio
	# sudo apt-get check


import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone() as source:
	print("Say things")
	audio = r.listen(source)
	try:
		text = r.recognize_google(audio, language="es-ES")
		print("You said : {}".format(text))
	except:
		print("SOMETHING HAPPENED")