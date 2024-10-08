Import speech_recognition as sr
import pyaudio

voz = sr.Recognizer()

while True:
	print('\nEscuchando....')
	texto = ''
	with sr.Microphone() as fuente:
		voz.adjust_for_ambient_noise(fuente)
		try:
			audio = voz.listen(fuente)
			texto = voz.recognize_google(audio, language="es-MX")
		except sr.UnknownValueError:
			pass
		except sr.RequestError
			pass
		except sr.WaitTimeoutError:
			pass
	print("\nDijiste", texto)
	if texto =="adios"
		print("\nHasta la vista baby\n")
		break
	
	print('\nTexto: ', texto)