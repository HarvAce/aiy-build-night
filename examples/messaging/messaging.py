#!/usr/bin/env python3
import platform
import urllib.parse
import subprocess
import sys
import _thread as thread
import http.client
from time import sleep
import RPi.GPIO as GPIO
import aiy.assistant.auth_helpers
from aiy.assistant.library import Assistant
import aiy.audio
import aiy.voicehat
from google.assistant.library.event import EventType

HOST = 'aiy-voice-208417.appspot.com'

LOCATION_CODE = 'hartford'
DESTINATION_CODE = 'stpaul'
DESTINATION_NAME = 'Saint Paul'

listening = False
speaking = False

def sendMessage(message):
    http.send(message)

def receiveMessage():
    client = http.client.HTTPSConnection(HOST)
    client.request('GET', '/message/' + LOCATION_CODE + '')
    data = client.getresponse().read().decode()
    if data != 'empty':
        while listening:
            print('listening...')
            sleep(0.5)
        speaking = True
        print(data)
        aiy.audio.say(data)
        speaking = False
    sleep(1)
    receiveMessage()

# Safely Remove Element From List
def remove(val, arr):
    try:
        arr.remove(val)
    except:
        pass

def process_event(assistant, event):
    if speaking:
        return

    # Controls Button Lighting
    status_ui = aiy.voicehat.get_status_ui()

    if event.type == EventType.ON_START_FINISHED:
        print('Say "OK, Google", and tell the other location something...')
        status_ui.status('ready')

        thread.start_new_thread(receiveMessage, ())

    elif event.type == EventType.ON_CONVERSATION_TURN_STARTED:
        listening = True
        status_ui.status('listening')
        
    elif event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED:
        # Stop Google Assistant Default Behaviour
        assistant.stop_conversation()

        # Get Command and Utterance
        splitString = event.args['text'].lower().split(' ')
        command = splitString[0]

        if command == 'tell':
            # Remove Command From Message
            remove('tell', splitString)

            # Remove Location From Message
            remove('hartford', splitString)
            remove('hertford', splitString) # Misheard 'hartford'
            remove('saint', splitString)
            remove('st.', splitString)
            remove('steve', splitString) # Misheard 'saint'
            remove('paul', splitString)

            print('/message/' + DESTINATION_CODE + '/' + ('%20'.join(splitString)))

            # Send Message to Server
            client = http.client.HTTPSConnection(HOST)
            client.request('GET', '/message/' + DESTINATION_CODE + '/' + ('%20'.join(splitString)))
            res = client.getresponse()
            print(res.status, res.reason)
            
            aiy.audio.say('Message sent to ' + DESTINATION_NAME)
            status_ui.status('ready')
            listening = False
        elif command == 'quit' or command == 'exit':
            status_ui.status('power-off')
            sleep(0.1)
            print('Goodbye')
            aiy.audio.say('Goodbye')
            sys.exit()
        else:
            listening = False

    # No Conversation, Go Back to Ready State
    elif (event.type == EventType.ON_CONVERSATION_TURN_FINISHED
          or event.type == EventType.ON_CONVERSATION_TURN_TIMEOUT
          or event.type == EventType.ON_NO_RESPONSE):
        status_ui.status('ready')
        listening = False

def main():
    # Turn Off Warning Flags
    GPIO.setwarnings(False)

    # Start Processing Google Assistant Events
    credentials = aiy.assistant.auth_helpers.get_assistant_credentials()
    with Assistant(credentials) as assistant:
        for event in assistant.start():
            process_event(assistant, event)

if __name__ == '__main__':
    main()