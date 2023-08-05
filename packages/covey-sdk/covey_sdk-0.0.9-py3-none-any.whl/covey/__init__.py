import os

_ROOT = os.path.abspath(os.path.dirname(__file__))

def get_data(path):
    return os.path.join(_ROOT, 'data', path)

def get_output(path):
    return os.path.join(_ROOT, 'output', path)

def get_checks(path):
    return os.path.join(_ROOT, 'checks', path)

