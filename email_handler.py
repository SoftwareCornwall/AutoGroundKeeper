# -*- coding: utf-8 -*-
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import email.utils
import smtplib

from os.path import basename
import subprocess
import re


class EmailHandler:
    def __init__(self, config):
        self._config = config
        #self.prefrences = config_handler.ConfigHandler()
        # self.prefrences.load("user_preferences")

    @staticmethod
    def mxlookup(domain):
        try:
            data = subprocess.getoutput('host ' + domain)
            data = re.findall('mail is handled by (.*?) (.*?)\n', data + '\n')
            return min([int(i[0]), i[1]] for i in data)[1]
        except ValueError:
            pass
        return domain

    @staticmethod
    def send_email_details(
            rcpttos,
            fromaddr,
            fromname,
            subject,
            body,
            attachments):

        mimeapps = []
        for f in attachments:
            try:
                with open(f, 'rb') as cfile:
                    app = MIMEApplication(cfile.read())
                    app['Content-Disposition'] = 'attachment; filename="%s"' % basename(
                        f)
                    mimeapps.append(app)
            except Exception as error:
                print(error)
        print('Fetched attachments')
        addrlist = {}
        for toaddr in rcpttos:
            try:
                server = EmailHandler.mxlookup(toaddr.split('@')[1])
                addrlist[server] = addrlist.get(server, []) + [toaddr]
            except IndexError:
                print('Invalid email:', toaddr)
        print('Looked up addresses')
        for server in addrlist:
            toaddrs = addrlist[server]
            msg = MIMEMultipart()
            msg['To'] = ', '.join(toaddrs)
            msg['From'] = email.utils.formataddr((fromname, fromaddr))
            msg['Subject'] = subject
            msg.attach(MIMEText(body))
            for app in mimeapps:
                msg.attach(app)
            try:
                smtp = smtplib.SMTP(server)
                print('Connected to', server)
                try:
                    smtp.starttls()
                    print('Started TLS')
                except Exception as error:
                    print(error)
                smtp.send_message(msg)
                print('Sent')
            except Exception as error:
                print(error)

    def send_email(self, subject, body, attachments):
        rcpttos = self._config.get_user_preferences('Send_To')
        fromaddr = self._config.get_user_preferences('From_Address')
        fromname = self._config.get_user_preferences('From_Name')
        self.send_email_details(
            rcpttos,
            fromaddr,
            fromname,
            subject,
            body,
            attachments)

    def testing(self):
        print(self._config.get_user_preferences('Send_To'))
