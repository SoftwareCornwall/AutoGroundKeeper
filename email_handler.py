# -*- coding: utf-8 -*-


class EmailHandler:
    def __init__(self, config):
        self._config = config

    def send(
            self,
            to_address,
            from_address,
            from_name,
            subject,
            body,
            attachments):
        print('To:', to_address)
        print('From: %s <%s>' % (from_name, from_address))
        print('Subject:', subject)
        print('Body:', body)
        print('Attachments:', attachments)
