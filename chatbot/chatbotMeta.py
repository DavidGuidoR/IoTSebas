# Use the native inference API to send a text message to Meta Llama 3.

import boto3
import json

from botocore.exceptions import ClientError

#---------------------------------------------------------------------
import speech_recognition as sr
import pyaudio
import logging
import os
#---------------------------------------------------------------------
import os
from playsound import playsound
from gtts import gTTS

import pyttsx3
#---------------------------------------------------------------------
voz = sr.Recognizer()
print('\nEscuchando....')
texto = ''
with sr.Microphone() as fuente:
    voz.adjust_for_ambient_noise(fuente)
    try:
        audio = voz.listen(fuente)
        texto = voz.recognize_google(audio, language="es-MX")
    except sr.UnknownValueError:
        pass
    except sr.RequestError:
        pass
    except sr.WaitTimeoutError:
        pass
    print("\nDijiste", texto)
    if texto =="adios":
        print("\nHasta la vista baby\n")
        
print('\nTexto: ', texto)

prompt = texto

#---------------------------------------------------------------------

# Create a Bedrock Runtime client in the AWS Region of your choice.
client = boto3.client("bedrock-runtime", region_name="us-east-1")

# Set the model ID, e.g., Llama 3 8b Instruct.
model_id = "meta.llama3-8b-instruct-v1:0"

# Embed the prompt in Llama 3's instruction format.
formatted_prompt = f"""
<|begin_of_text|>
<|start_header_id|>user<|end_header_id|>
{prompt}
<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
"""

# Format the request payload using the model's native structure.
native_request = {
    "prompt": formatted_prompt,
    "max_gen_len": 512,
    "temperature": 0.5,
}

# Convert the native request to JSON.
request = json.dumps(native_request)

try:
    # Invoke the model with the request.
    response = client.invoke_model(modelId=model_id, body=request)

except (ClientError, Exception) as e:
    print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
    exit(1)

# Decode the response body.
model_response = json.loads(response["body"].read())

# Extract and print the response text.
response_text = model_response["generation"]
print(response_text)

#---------------------------------------------------------------
# Reemplazo de gTTS por espeak para la sï¿½ntesis de voz
os.system(f'espeak -v es "{response_text}" --stdout > voz.wav')

# Reproducciï¿½n del archivo de audio
os.system("aplay voz.wav")