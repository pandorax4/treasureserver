import os
import subprocess
import time,threading

__commit_busy = False

def to_publish():
    global __commit_busy
    work_dir = '/home/fredshao/game/geekcashlucky.github.io'
    os.chdir(work_dir)

    # git add .
    command_add = ['git','add','.']
    # git commit -m "Update"
    command_commit = ['git','commit','-m','"Update"']
    # git push origin master
    command_push = ['git','push','origin','master']

    try:
        out_bytes = subprocess.check_output(command_add,stderr=subprocess.STDOUT)
        out_str = out_bytes.decode('utf-8')
        print(out_str)

        out_bytes = subprocess.check_output(command_commit,stderr=subprocess.STDOUT)
        out_str = out_bytes.decode('utf-8')
        print(out_str)

        out_bytes = subprocess.check_output(command_push,stderr=subprocess.STDOUT)
        out_str = out_bytes.decode('utf-8')
        print(out_str)
        __commit_busy = False
    except Exception as e:
        __commit_busy = False
        print("EXCEPTION: ",e)
        

def publish():
    global __commit_busy
    if __commit_busy:
        print("Commit Busy")
        return
    __commit_busy = True
    t = threading.Thread(target=to_publish,name='topublish')
    t.start()


#publish()