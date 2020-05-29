import os

root_dir = os.path.dirname(os.path.abspath(__file__))

def get_dirname(f):
    return os.path.basename(os.path.dirname(f))

def plot_dir(f):
    return root_dir+"/target/plot/" + get_dirname(f) + "/"

def data_dir(f):
    return root_dir+"/target/data/" + get_dirname(f) + "/"