#!/usr/bin/env python3

###########################
# this script uses pipenv #
###########################

import ap_config as cfg
import sh
import io
import ap_email
if __name__ == '__main__':
    print('Autocompile.py is running...')
    tryTimes = 1
    while tryTimes <= cfg.maxTryTimes:
        try:
            sh.cd(cfg.globalCwd)

            stdoutput = io.StringIO()
            sh.ls('-d',sh.glob('*/') ,_out=stdoutput)
            dirs = [ _[:-1] for _ in stdoutput.getvalue().split()]
            nameIsIn = False
            for x in dirs:
                if x == cfg.projectname:
                    nameIsIn = True
                    break
        
            if nameIsIn == True:
                print("Remove old ", cfg.projectname)
                sh.rm('-r', cfg.projectname)

            sh.git.clone(cfg.repository)
            sh.cd(cfg.projectname)
            sh.cmake('.')
            sh.make('-j{}'.format(cfg.thread))
            break
        except Exception as e:
            print("Build Failed")
            print("Try : ", tryTimes)
            print('Exception Caught:', e)
            print("Sending Email to Admins...")
            
            tryTimes += 1
            
            if tryTimes == cfg.maxTryTimes:
                addtionalMsg = 'Try times used up, Fatal error, exit...'    
            else:
                addtionalMsg = 'This is try:{}, it is going to retry...'.format(tryTimes)
            
                sh.cd(cfg.globalCwd)
                sh.rm('-r', cfg.projectname)

            ret = ap_email.sendNotifyMail("Autopile Error", exceptionMsg=e.args[0], 
                addtionalMsg=repr(e) + '\n' + addtionalMsg)
            if ret:
                print("Sending Email to Admins successful.")
            else:
                print("Sending Failed. exit")
                exit(1)

    if tryTimes > cfg.maxTryTimes:
        exit(2)

    
    print("Build successful")
    print("Sending Email to admins...")
    ap_email.sendNotifyMail("Autopile Build Successful")



