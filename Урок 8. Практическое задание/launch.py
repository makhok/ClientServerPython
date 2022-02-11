"""Лаунчер"""

import subprocess

subprocess.Popen('python server.py', creationflags=subprocess.CREATE_NEW_CONSOLE)

subprocess.Popen('python client.py', creationflags=subprocess.CREATE_NEW_CONSOLE)
subprocess.Popen('python client.py', creationflags=subprocess.CREATE_NEW_CONSOLE)

