# -*- coding: utf-8 -*-
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import email.utils
import smtplib

from os.path import basename
import subprocess
import re

import socket
import time


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
            return tuple([i[1] for i in sorted(data, key=lambda x: int(x[0]))])
        except ValueError:
            pass
        return (domain, )

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
        success = True
        for server_list in addrlist:
            toaddrs = addrlist[server_list]
            msg = MIMEMultipart()
            msg['To'] = ', '.join(toaddrs)
            msg['From'] = email.utils.formataddr((fromname, fromaddr))
            msg['Subject'] = subject
            msg.attach(MIMEText(body))
            for app in mimeapps:
                msg.attach(app)
            local_success = False
            print(','.join(server_list))
            for server in server_list:
                try:
                    smtp = smtplib.SMTP(server)
                    print('Connected to', server)
                    try:
                        smtp.starttls()
                        print('Started TLS')
                    except smtplib.SMTPNotSupportedError as error:
                        print(error)
                    smtp.send_message(msg)
                    print('Sent')
                    local_success = True
                    break
                except socket.gaierror as error:
                    pass
            success &= local_success
        return success

    def send_email(self, subject, body, attachments, schedule, resend=True):
        rcpttos = self._config.get_user_preferences('Send_To')
        fromaddr = self._config.get_user_preferences('From_Address')
        fromname = self._config.get_user_preferences('From_Name')
        if not self.send_email_details(
                rcpttos,
                fromaddr,
                fromname,
                subject,
                body,
                attachments) and resend:
            print('Sending failed, so resending again soon')
            schedule.register_task(
                'resend',
                self.send_email,
                (subject,
                 body,
                 attachments,
                 schedule),
                time.time() + 20)

    def testing(self):
        print(self._config.get_user_preferences('Send_To'))
