import os.path
from constants import ROOT_PATH


def resolve_path(*paths):
    return os.path.join(ROOT_PATH, *paths)


def get_sample_path(*paths):
    return resolve_path("samples", *paths)


def get_temp_path(*paths):
    return resolve_path("temp", *paths)


def get_workspace_path(*paths):
    return resolve_path("workspace", *paths)


def get_content_path(*paths):
    return resolve_path("content", *paths)


os.makedirs(get_sample_path(), exist_ok=True)
os.makedirs(get_temp_path(), exist_ok=True)
os.makedirs(get_workspace_path(), exist_ok=True)
os.makedirs(get_content_path(), exist_ok=True)
