import speech_recognition as sr
import pyaudio

voz = sr.Recognizer()

print('\nEscuchando....')

with sr.Microphone() as fuente:
	voz.adjust_for_ambient_noise(fuente)
	audio = voz.listen(fuente)
	texto = voz.recognize_google(audio)
	
print('\nTexto: ', texto)