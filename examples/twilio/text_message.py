#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import platform
import subprocess
import sys

import aiy.assistant.auth_helpers
from aiy.assistant.library import Assistant
import aiy.audio
import aiy.voicehat
from google.assistant.library.event import EventType
from twilio.rest import Client

logging.basicConfig(
   level=logging.INFO,
   format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
)


def send_text():
   # Your Account Sid and Auth Token from twilio.com/console<http://twilio.com/console>
   account_sid = 'INSERT_YOUR_SID_HERE'
   auth_token = 'INSERT_YOUR_TOKEN_HERE'
   client = Client(account_sid, auth_token)

   message = client.messages.create(
                             body='Hello there from Google AIY!',
                             from_='+INSERT_TWILIO_NUMBER_HERE',
                             to='+INSERT_PHONE_NUMBER_HERE'
                         )

   print(message.sid)
   aiy.audio.say('I have sent your messsage via Twilio!')


def process_event(assistant, event):
   status_ui = aiy.voicehat.get_status_ui()
   if event.type == EventType.ON_START_FINISHED:
       status_ui.status('ready')
       if sys.stdout.isatty():
           print('Say "OK, Google" then speak, or press Ctrl+C to quit...')

   elif event.type == EventType.ON_CONVERSATION_TURN_STARTED:
       status_ui.status('listening')

   elif event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED and event.args:
       print('You said:', event.args['text'])
       text = event.args['text'].lower()
       if text == 'send text message':
           assistant.stop_conversation()
           send_text()
       elif text != 'send Twilio text message text message':
           aiy.audio.say('Sorry, I can only send Twilio messages')


   elif event.type == EventType.ON_END_OF_UTTERANCE:
       status_ui.status('thinking')

   elif (event.type == EventType.ON_CONVERSATION_TURN_FINISHED
         or event.type == EventType.ON_CONVERSATION_TURN_TIMEOUT
         or event.type == EventType.ON_NO_RESPONSE):
       status_ui.status('ready')

   elif event.type == EventType.ON_ASSISTANT_ERROR and event.args and event.args['is_fatal']:
       sys.exit(1)


def main():
   if platform.machine() == 'armv6l':
       print('Cannot run hotword demo on Pi Zero!')
       exit(-1)

   credentials = aiy.assistant.auth_helpers.get_assistant_credentials()
   with Assistant(credentials) as assistant:
       for event in assistant.start():
           process_event(assistant, event)


if __name__ == '__main__':
   main()
