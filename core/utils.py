import os

def is_project_folder(path):
    return os.path.isfile(os.path.join(path, ".projectmeta"))
