import os
import subprocess
import time

PROCESS = []

while True:
    ACTION = input('Choose an action: q - exit, '
                   's - run server and clients, x - close all windows: ')

    if ACTION == 'q':
        break
    elif ACTION == 's':
        catalog = os.getcwd()
        p = f'python "{catalog}/server.py"'
        PROCESS.append(subprocess.Popen([
            'xterm',
            '-e',
            p])
        )
        print(p)
        time.sleep(0.1)
        for i in range(3):
            p = f'python "{catalog}/client.py" -n test{i}'
            PROCESS.append(subprocess.Popen([
                'xterm',
                '-hold',
                '-e',
                p])
            )
            print(p)
            time.sleep(0.1)
    elif ACTION == 'x':
        while PROCESS:
            VICTIM = PROCESS.pop()
            VICTIM.kill()
