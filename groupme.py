from urllib.parse import urlencode
from urllib.request import Request, urlopen
import requests
from flask import Flask, request
import os

class GroupmeBot():
    def __init__(self, in_bot_id):
        self.bot_id = in_bot_id

    # Send a message in the groupchat
    def reply(self, msg):
        url = 'https://api.groupme.com/v3/bots/post'
        data = {
            'bot_id'        : self.bot_id,
            'text'          : msg
        }
        request = Request(url, urlencode(data).encode())
        json = urlopen(request).read().decode()
        return json

    # Send a message with an image attached in the groupchat
    def reply_with_image(self, msg, imgURL):
        url = 'https://api.groupme.com/v3/bots/post'
        urlOnGroupMeService = self.upload_image_to_groupme(imgURL)
        data = {
            'bot_id'        : self.bot_id,
            'text'            : msg,
            'picture_url'    : urlOnGroupMeService
        }
        request = Request(url, urlencode(data).encode())
        json = urlopen(request).read().decode()
        return json
        
    # Uploads image to GroupMe's services and returns the new URL
    def upload_image_to_groupme(self, imgURL):
        imgRequest = requests.get(imgURL, stream=True)
        filename = 'temp.png'
        postImage = None
        if imgRequest.status_code == 200:
            # Save Image
            with open(filename, 'wb') as image:
                for chunk in imgRequest:
                    image.write(chunk)
            # Send Image
            headers = {'content-type': 'application/json'}
            url = 'https://image.groupme.com/pictures'
            files = {'file': open(filename, 'rb')}
            payload = {'access_token': 'eo7JS8SGD49rKodcvUHPyFRnSWH1IVeZyOqUMrxU'}
            r = requests.post(url, files=files, params=payload)
            imageurl = r.json()['payload']['url']
            os.remove(filename)
            return imageurl

    # Checks whether the message sender is a bot
    def sender_is_bot(self, message):
        return message['sender_type'] == "bot"
