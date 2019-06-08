#!/usr/bin/env python3

###########################
# this script uses pipenv #
###########################

import ap_config as cfg
import sh
import io
import ap_email
import time

def exitWithEMailSent(mailSubject, mailBody, exitCode):
    pass
    try:
        ap_email.sendMail(mailSubject, mailBody)
    except Exception as e:
        print("Exception caught in exitWithEMailSent(), exit(1)")
        exit(1)

    exit(exitCode)




if __name__ == '__main__':
    print('Autocompile.py is running...')
    #cfg.Context('test')
    cfg.Context('utbasecode')
    tryTimes = 1
    mailContent = ''

    gitCloneSuccFlag = False
    cmakeSuccFlag = False
    makeSuccFlag = False

    sh.cd(cfg.globalCwd)

    stdoutput = io.StringIO()
    sh.ls('-d',sh.glob('*/') ,_out=stdoutput)
    dirs = [ _[:-1] for _ in stdoutput.getvalue().split()]


    if cfg.projectname in dirs:
        print("Old " + cfg.projectname + ' Found, remove it')
        sh.rm('-r', cfg.projectname)


    while tryTimes <= cfg.maxTryTimes:
        try:

            if gitCloneSuccFlag:
                print("git clone, successed, skip")
            else:
                #sh.contrib.git.clone(cfg.repository)
                gitCloneSuccFlag = True

            sh.cd(cfg.projectname)

            if cmakeSuccFlag:
                print("cmake, successed, skip")
            else:
                sh.cmake('.')
                cmakeSuccFlag = True

            if makeSuccFlag:
                print("make, successed, skip")
            else:
                sh.make('-j{}'.format(cfg.thread))
                makeSuccFlag = True

            break
        except Exception as e:
            print("Build Failed")
            print("Try : ", tryTimes)
            print('Exception Caught:', e)
            
            
            addtionalMsg = 'This is try:{} failed, it is going to retry...'.format(tryTimes) + '\n'
            addtionalMsg += 'git clone status:' + str(gitCloneSuccFlag) + '\n' + \
                'cmake status: ' + str(cmakeSuccFlag) + '\n' + \
                'make status: ' + str(makeSuccFlag) + '\n'
            tryTimes += 1
            sh.cd(cfg.globalCwd)
            sh.rm('-rf', cfg.projectname)

            mailContent += ap_email.generateNotifyText("Autopile Error", exceptionMsg=str(e) + '\n' + repr(e), addtionalMsg=addtionalMsg)
            time.sleep(1)

    if tryTimes > cfg.maxTryTimes:
        print("MaxTryTime Reached, Sending EMail to admins, exit(2)")
        mailContent += "MaxTryTime Reached, exit(2)"
        exitWithEMailSent("Autopile Log", mailContent, 2)

    
    print("Build successful")
    print("Sending Email to admins...")
    mailContent += ap_email.generateNotifyText("Autopile Build successful")
    exitWithEMailSent("Autopile Log", mailContent, 0)


