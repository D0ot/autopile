#!python3

##########################
# this script use pipenv #
##########################

import ap_config as cfg
import sh
import io
if __name__ == '__main__':
    print('Autocompile.py is running...')
    try:
        stdoutput = io.StringIO()
        sh.ls(_out=stdoutput)
        print(stdoutput.getvalue())
        sh.git.clone(cfg.repository)
        sh.cd(cfg.projectname)
        
    except Exception as e:
        print('Exception', e)
        exit(1)
