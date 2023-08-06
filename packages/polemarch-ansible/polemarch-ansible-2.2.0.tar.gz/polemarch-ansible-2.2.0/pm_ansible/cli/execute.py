import os
import sys
import signal
import subprocess
from .base import get_parser


ON_POSIX = 'posix' in sys.builtin_module_names


def get_ansible_command(command):
    python_exec_dir = os.path.dirname(sys.executable)
    new_command = '{}/{}'.format(python_exec_dir, command)
    if os.path.exists(new_command):
        command = new_command
    return command


def print_output(output):
    if output:
        try:
            output = output.decode('utf-8')
        except:  # nocv
            # No coverage because depend on LC_ALL and LANG env variables
            return False
        print(output, end='')
        sys.stdout.flush()
    return True


def handler(args=sys.argv[1:], parser=get_parser()):
    command, arguments = get_ansible_command(args[0]), args[1:]
    os.environ.setdefault('ANSIBLE_FORCE_COLOR', 'true')
    process = subprocess.Popen(
        [command] + arguments,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        bufsize=0, env=os.environ.copy(), close_fds=ON_POSIX,
    )
    os.kill(process.pid, signal.SIG_DFL)
    rc = None
    while True:
        output = process.stdout.read(1)
        if rc is not None:
            output += process.stdout.read()
            print_output(output)
            break
        if not print_output(output):
            # No coverage because depend on LC_ALL and LANG env variables
            continue  # nocv
        rc = process.poll()

    process.stdout.close()
    sys.exit(rc) if rc else None
