#!/usr/bin/env python3
###########################
#  This script use pipenv #
###########################


import ap_config as cfg
import smtplib
import time
import socket
from email.header import Header
from email.mime.text import MIMEText


def sendNotifyMail(briefError,* , whichMachine = socket.gethostname(),timeStamp=time.ctime() , exceptionMsg='' , addtionalMsg=''): 
    msgBody = briefError + '\n'
    msgBody += 'Timestamp : ' + timeStamp + '\n'

    if exceptionMsg != '':
        msgBody += 'Exception Message : ' + exceptionMsg + '\n'
    
    if addtionalMsg != '':
        msgBody += 'Addtional Messages : ' + addtionalMsg

    errorMsg = MIMEText(msgBody, 'plain', 'utf-8')
    errorMsg['From'] = whichMachine + '<' + cfg.sender + '>'
    recList = 'Receivers' + '<'
    for x in cfg.receivers:
        recList += x + ','

    recList = recList[:-1]


    errorMsg['To'] = recList + '>'
    errorMsg['Subject'] = Header(briefError, 'utf-8')
    errorMsg['Cc'] = cfg.sender

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
        smtp.sendmail(cfg.sender, cfg.receivers, errorMsg.as_string())
        
    except smtplib.SMTPException as e:
        print(e)
        sucFlag = False
    
    return sucFlag


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
