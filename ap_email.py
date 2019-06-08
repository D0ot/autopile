#!/usr/bin/env python3
############################
#  This script uses pipenv #
############################


import ap_config as cfg
import smtplib
import time
import socket
from email.header import Header
from email.mime.text import MIMEText


def generateNotifyText(briefError, *, timeStamp=time.ctime() , exceptionMsg='' , addtionalMsg=''):
    msgBody = '*'*50 + '\n'
    msgBody += briefError + '\n'
    msgBody += 'Timestamp : ' + timeStamp + '\n'

    if exceptionMsg != '':
        msgBody += '-'*20 + '\n'
        msgBody += 'Exception Message : ' + exceptionMsg + '\n'+ '-'*20 + '\n'
    
    if addtionalMsg != '':
        msgBody += 'Addtional Messages : ' + addtionalMsg
    msgBody += '*'*50 + '\n'
    return msgBody





def sendNotifyMail(briefError,* , whichMachine = socket.gethostname(),timeStamp=time.ctime() , exceptionMsg='' , addtionalMsg=''): 
    msgBody = generateNotifyText(briefError, exceptionMsg=exceptionMsg, addtionalMsg=addtionalMsg)
    return sendMail(briefError, msgBody, whichMachine)





def sendMail(mailSubject, mailBody, mailSenderName = socket.gethostname()):
    msg = MIMEText(mailBody, 'plain', 'utf-8')
    msg['From'] = mailSenderName + '<'  + cfg.sender + '>'
    msg['To'] = '<' + ','.join(cfg.receivers) + '>'
    msg['Subject'] = Header(mailSubject, 'utf-8')
    msg['Cc'] = cfg.sender

    sucFlag = True

    try:
        smtp = None
        if cfg.smtpServer.find('office365') != -1:
            smtp = smtplib.SMTP('{}:{}'.format(cfg.smtpServer, cfg.smtpServerPort))
            smtp.ehlo()
            smtp.starttls()
        else:
            smtp = smtplib.SMTP()
            smtp.connect(cfg.smtpServer)
        smtp.login(cfg.username, cfg.password)
        smtp.sendmail(cfg.sender, cfg.receivers, msg.as_string())
        
    except smtplib.SMTPException as e:
        print(e)
        sucFlag = False
    
    return sucFlag


# TODO
def sendMailWithFile(mailSubject, mailBody, mailSenderName, mailFileName):
    pass



# This may not work for outlook
def sendExample():
    message = MIMEText('Hello from python with smtplib', 'plain', 'utf-8')
    message['From'] = "Sender" + '<' + cfg.sender + '>'
    message['To'] = "Receiver" + '<' + cfg.receivers[0] + '>'
    message['Subject'] = Header('mail_title', 'utf-8')
    message['Cc'] = cfg.sender

    try:
        smtp = smtplib.SMTP()
        smtp.connect(cfg.smtpServer)
        smtp.login(cfg.username, cfg.password)
        smtp.sendmail(cfg.sender, cfg.receivers, message.as_string())
        print("Test E-Mail Successful")        
    except smtplib.SMTPException as e:
        print("Sending Faile", e)


# this is for test
if __name__ == '__main__':

    ret = sendNotifyMail('BriefError', addtionalMsg="adderror", exceptionMsg="excp")
    if ret:
        print("sendErrorMail successed")
    else:
        print("sendErrorMail failed")
