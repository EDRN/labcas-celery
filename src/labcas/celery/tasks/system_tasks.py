'''
Module containing LabCAS Celery tasks.
'''

from labcas.celery.worker import app
import subprocess
import io


def exec_subprocess(command):
    '''
    Executes a generic system command as a subprocess.
    The command must be supplied as a list of strings.
    '''

    print("Executing command: %s" % " ".join(command))
    proc = subprocess.Popen(command,
                            stdout=subprocess.PIPE,
                            # merge stderr to stdout
                            stderr=subprocess.STDOUT
                            )
    # echo output as it is produced
    for line in io.TextIOWrapper(proc.stdout, encoding="utf-8"):
        print(line)
    # wait for the sub-process to finish
    proc.wait()

    print("Command exited with code: %s" % proc.returncode)
    return proc.returncode


@app.task
def exec_command(command):
    '''
    Task to execute a generic system command.
    Command is passed as a single string.
    '''

    return exec_subprocess(command.split(" "))


@app.task
def exec_script(script_path, *argv, **kwargs):
    '''
    Task to execute a generic script with input arguments.
    '''

    command = [script_path] + list(argv) + [
        "%s=%s" % (k, v) for k, v in kwargs.items()]

    return exec_subprocess(command)
