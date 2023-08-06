#!/usr/bin/python
# coding:utf-8
#
# e-mail sender
#
# version 0.5 2021.5.1
#
# required package:  smtplib
#
# please install PyEmail which include smtplib
#
# pip install PyEmail
#
#  Usage Example
#
# username = 'xxxxxxx@qq.com'  # username to login SMTP server
# password = 'xxxxxxxxxx'      # password to login SMTP server
#
# receiver = 'xxxxxxxx@qq.com'  # receiver of the mail
#
# # Create mail object
# mail = Mail(username, password)
#
# try:
#     # email title
#     mail_subject = "Different world 3"
#
#     # we can embed the attachment as an image by referring image to src= “cid:0”
#     mail_body = "Different world<img src='cid:0'>"
#
#     # send mail, with file attachment
#     mail.send([receiver], mail_subject, mail_body, ['1.jpg'])
#
#     print("send mail OK")
#
# except smtplib.SMTPException as e:
#     # when send error
#     print("ERROR:" + str(e))
#
#

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase
from email.header import Header
import os
import sys
import json


class Mail:

    """
    A class to send e-mail.

    :Chinese: 发送邮件的类

    ------------------

    # Usage Example:


    # create object

    mail = Mail('sender@host.com', passwd, host='smtp.host.com', sender='sender@host.com')

    # send

    mail.send(['receiver@some.com'], 'the title', 'content text', [filename1, filename2])

    """

    def __init__(self, user, passwd, sender=None, host=None):
        """
        create instance of Mail

        :param user:   username to login SMTP server
        :param passwd: password to login SMTP server
        :param host:   (optional) SMTP server. if empty, detect host by the user parameter.
        :param sender: (optional) sender of the mail. if empty, use the user parameter
        """

        self.user = user      # username to login host
        self.passwd = passwd  # password to login host
        self.host = host      # SMTP server
        self.sender = sender  # sender of the mail

        if sender is None or sender == '':
            self.sender = self.user

        if (host is None or host == '') and user.find('@') > 0:
            host = 'smtp.' + user[user.find('@') + 1:]
            self.host = host

    def send(self, receivers: list, subject: str, body: str, attach_filenames: list = None):
        """
        send a mail

        :param receivers:  list of the e-mail addresses of receivers
        :param subject:    title of the mail
        :param body:    content of the mail
        :param attach_filenames:      (optional) attachment file name list
        
        :return: return True if success, return SMTPException object if failed.
        """
        # SEE: https://www.code-learner.com/python-send-html-image-and-attachment-email-example/

        # validate params
        if isinstance(receivers, str):
            receivers = [receivers]
        if isinstance(receivers, list):
            receivers = '; '.join(receivers)
        else:
            raise ValueError('argument receiver invalid')

        if attach_filenames is None:
            attach_filenames = []

        if isinstance(attach_filenames, str):
            attach_filenames = [attach_filenames]

        if not isinstance(attach_filenames, list):
            raise smtplib.SMTPException('Mail.send() parameter attach_filenames must be a list of filenames')

        # compose mail message
        msg = MIMEMultipart()
        msg['From'] = self.sender
        msg['To'] = receivers
        msg['Subject'] = str(subject)
        msg.attach(MIMEText(str(body), 'html'))

        # add attachment files
        if isinstance(attach_filenames, list):
            count = 0
            for file in attach_filenames:
                file = file.strip(' ')
                if os.path.exists(file):
                    # set attachment mime type
                    mime = MIMEBase("application", "octet-stream")
                    # another example: mime = MIMEBase('image', 'png', filename='img1.png')

                    # read attachment file content into the MIMEBase object
                    mime.set_payload(open(file, "rb").read())

                    # add required header data
                    mime.add_header("Content-Disposition", "attachment",
                                    filename=Header(os.path.basename(file), "utf-8").encode())
                    mime.add_header('X-Attachment-Id', str(count))
                    mime.add_header('Content-ID', '<' + str(count) + '>')  # cid

                    # encode with base64
                    encoders.encode_base64(mime)

                    # add MIMEBase object to MIMEMultipart object
                    msg.attach(mime)

                    count += 1
                else:
                    raise smtplib.SMTPException('Mail.send() attachment file ' + str(file) + ' do not exists')

        smtp_obj = smtplib.SMTP(self.host)
        smtp_obj.login(self.user, self.passwd)
        smtp_obj.sendmail(self.sender, receivers, msg.as_string())
        return True


def _cmd_set_mail_settings():
    """ command line set mail settings """
    if len(sys.argv) > 3:
        user = sys.argv[2]
        passwd = sys.argv[3]
        data = {'user': user, 'passwd': passwd}
        f = open('mail.setting', 'w')
        f.write(json.dumps(data))
        f.close()
        sys.stdout.write('mail setting saved\n');
    else:
        sys.stdout.write("Usage: python mail.py set username password\n")


def _cmd_send_mail():
    """ command line send mail """
    if len(sys.argv) < 4:
        sys.stdout.write("Usage: python mail.py sent receiver subject body attach_file\n")
        exit()

    # read parameters
    receiver = sys.argv[2]
    subject = sys.argv[3]
    body = sys.argv[4] if len(sys.argv) > 4 else ''
    attach = sys.argv[5] if len(sys.argv) > 5 else []

    # check mail.setting file exists
    if not os.path.exists('mail.setting'):
        sys.stdout.write("Missing settings, please set first:  python mail.py set username password\n")
        exit()

    # load mail setting
    # noinspection PyBroadException
    try:
        f = open('mail.setting', 'r')
        data = f.read()
        f.close()
        data = json.loads(data)
        user = data['user']
        passwd = data['passwd']
    except Exception:
        sys.stdout.write("Error settings, please set first:  python mail.py set username password\n")
        exit()

    # send mail
    # noinspection PyBroadException
    try:
        m = Mail(user, passwd)
        if m.send(receiver, subject, body, attach):
            sys.stdout.write("mail sent to " + receiver + '\n')
    except Exception as e:
        sys.stdout.write("error send mail, " + str(e) + '\n')


def _cmd_print_usage():
    """ command line print usage"""
    sys.stdout.write("Python mail package, Version 0.5, JoStudio\n\n")
    sys.stdout.write("Usage example:\n\n")
    sys.stdout.write("    # set username and passwd to login the SMTP server before send mail\n")
    sys.stdout.write("    python mail.py set username passwd\n\n")
    sys.stdout.write("    # send mail\n")
    sys.stdout.write("    python mail.py send receiver subject body attach_file\n\n")


if __name__ == '__main__':
    # command line operation
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == 'set':
            _cmd_set_mail_settings()

        elif command == 'send':
            _cmd_send_mail()

        else:
            _cmd_print_usage()
    else:
        _cmd_print_usage()




