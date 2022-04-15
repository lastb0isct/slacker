import os
import sys
import re
import yaml
import requests
import json
from aiosmtpd.handlers import Message


class MessageHandler(Message):
    print("MessageHandler was called")
    def __init__(self, *args, **kargs):
        Message.__init__(self, *args, **kargs)

        config = os.getenv('CONFIG', '/etc/slacker/config.yml')
        print(config)
        if not os.path.exists(config):
            print('Config doesn\'t exists!')
            exit(1)

        self.config = yaml.safe_load(open(config))

    def handle_message(self, message):
        """ This method will be called by aiosmtpd server when new mail will
            arrived.
        """

        self.send_to_slack(message)

    def send_to_slack(self, message):

        subject = (message['Subject'])
        sender = (message['From'])

        url = 'https://hooks.slack.com/services/'
        slack_data = {
            "username": "SMTPtoSlack",
            "icon_emoji": ":satellite:",
            #"channel" : "#somerandomcahnnel",
            "attachments": [
                {
                    "color": "#9733EE",
                    "fields": [
                        {
                            "title": sender,
                            "value": subject,
                            "short": "false",
                        }
                    ]
                }
             ]
        }

        byte_length = str(sys.getsizeof(slack_data))
        headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
        response = requests.post(url, data=json.dumps(slack_data), headers=headers)
        if response.status_code !=200:
            raise Exception(response.status_code, response.text)
