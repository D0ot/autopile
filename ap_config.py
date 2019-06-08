#!/usr/bin/env python3
############################
#  This script uses pipenv #
############################

# This is a config file for Autopile
# global 
log = False
logFile = ''
maxTryTimes = 10


# configure for main scripts 
globalCwd = '/home/doot/robocup3d/autopile'
repository = 'git@github.com:D0ot/Learnse.git'
projectname = 'Learnse'
# make -j(thread)
thread = 14


# configure for ap_email.py
# when an error occours receivers will get nofified.
smtpServer = 'smtp.office365.com'
smtpServerPort = 587
sender = 'robocup3dnotify@outlook.com'
receivers = ['1306793135@qq.com']
username = 'robocup3dnotify@outlook.com'

# it is not real password, it is just a permission code
password = 'robocup3d' 

# add sended self to receiver ie. Cc
# or it will get blocked smtp.163.com, FXXK 163's spam detect system
if smtpServer.find('@163.com') != -1 :
    receivers += [sender]


def Context(context):

    global maxTryTimes, repository, projectname

    if context == 'test':
        maxTryTimes = 3

    if context == 'utbasecode':
        maxTryTimes = 3
        repository = 'git@github.com:LARG/utaustinvilla3d.git'
        projectname = 'utaustinvilla3d'

    if context == 'log':
        log = True
        logFile = './log.txt'


if __name__ == '__main__':
    print("ap_config.py is just configure file, exit...")
    exit(0)


