import os
import re
import yaml
import requests
import json
from aiosmtpd.handlers import Message


class MessageHandler(Message):
    def __init__(self, *args, **kargs):
        Message.__init__(self, *args, **kargs)

        config = os.getenv('CONFIG', '/etc/slacker/config.yml')
        print(config)
        if not os.path.exists(config):
            print('Config doesn\'t exists!')
            exit(1)

        self.config = yaml.safe_load(open(config))

    def handle_message(self, message):
        print('This is calling handle_message')
        """ This method will be called by aiosmtpd server when new mail will
            arrived.
        """
        options = self.process_rules(message)

        print('matched', options)
        self.send_to_slack(self.extract_text(message), **options)

    def process_rules(self, message):
        """ Check every rule from config and returns options from matched
        """
        default = self.config['default']

        fields = {
            'from': message['From'],
            'to': message['To'],
            'subject': message['Subject'],
            'body': message.get_payload()
        }

        print(fields)

        return default

    def extract_text(self, message):
        fmt = self.config['default'].get('format', '%(body)s')
        body = message.get_payload()
        subject = message['Subject']
        return fmt % dict(body=body, subject=subject)

    def send_to_slack(self, text, **options):
        print('sending to slack', text)

        emailtext = {"email": text}
        return requests.post(url, json.dumps(emailtext))
