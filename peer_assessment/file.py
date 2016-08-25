import yaml


def get_users(filename):

    with open(filename) as f:
        users = yaml.load(f.read())
    return users['jupyterhub_users']

