import socket
import os
import logging
from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter
import ssl as ssl_lib
import certifi
#from onboarding_tutorial import OnboardingTutorial

app = Flask(__name__)
#slack signing secret
slack_events_adapter = SlackEventAdapter("86ccab", "/slack/events", app)
slack_web_client = WebClient(token="xoxb-872")
host = socket.gethostname()


@slack_events_adapter.on("team_join")
def onboarding_message(payload):
    event = payload.get("event", {})
    user_id = event.get("user", {}).get("id")
    response = slack_web_client.im_open(user_id)
    channel = response["channel"]["id"]
    slack_web_client.chat_postMessage(channel=channel,text=host+": :thinking_face:")

@slack_events_adapter.on("reaction_added")
def update_emoji(payload):
    event = payload.get("event", {})
    channel_id = event.get("item", {}).get("channel")
    user_id = event.get("user")
    slack_web_client.chat_postMessage(channel=channel_id,text=host+": :face_with_rolling_eyes:")

def palindrome(palabra):
    palabra_no_espacios = palabra.replace(" ","").upper()
    palabra = palabra_no_espacios
    L = len(palabra)
    T = 0
    for i in range(0,L):
       print(palabra[i],"=",palabra[L-1-i])
       if palabra[i] == palabra[L-1-i]:
          T = T + 1
    if T == L:
       return "Palíndrome"
    else:
       return "No Palíndrome"


@slack_events_adapter.on("message")
def message(payload):
    event = payload.get("event", {})
    channel_id = event.get("channel")
    user_id = event.get("user")
    text = event.get("text")
#    ts = event.get("ts")
    ts = ""
    if text != None and user_id != "UV84PJNSC":
        print("New message: "+text+" user: "+user_id) 
        if text == "negro":
            slack_web_client.chat_postMessage(channel=channel_id,text="Va no seas racista :triumph:",thread_ts=ts)
        else:
            slack_web_client.chat_postMessage(channel=channel_id,text=host+": te conteste :smiley:",thread_ts=ts)
            slack_web_client.chat_postMessage(channel=channel_id,text=palindrome(text),thread_ts=ts)


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    ssl_context = ssl_lib.create_default_context(cafile=certifi.where())
    app.run(host='0.0.0.0',port=5000, debug=True)
