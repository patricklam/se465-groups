import logging
import os
import subprocess

from django_gitolite.utils import home_dir

logger = logging.getLogger('se465')

def gitolite_creator_call(command):
    try:
        try:
            from subprocess import DEVNULL # py3k
        except ImportError:
            import os
            DEVNULL = open(os.devnull, 'wb')
        subprocess.check_call('ssh git@ecgit.uwaterloo.ca ' + command,
                              shell=True,
                              stdout=DEVNULL,
                              stderr=subprocess.STDOUT,
                              close_fds=True)
    except subprocess.CalledProcessError as e:
        msg = "command '{}' returned {}"
        logger.error(msg.format(e.cmd, e.returncode))

def is_se465_student(username):
    command = ['ssh', 'git@ecgit.uwaterloo.ca', 'list-memberships', '-u', username]
    try:
        from subprocess import DEVNULL # py3k
    except ImportError:
        import os
        DEVNULL = open(os.devnull, 'wb')
    o = subprocess.check_output(command, stderr=DEVNULL,
                                universal_newlines=True)
    for l in o.splitlines():
        if l == '@se465-1151-students':
            return True
    return False
