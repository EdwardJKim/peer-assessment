import hashlib
import os
import shutil
import random

from pgrader.names_generator import get_random_name
from pgrader.merge import read_notebook, write_notebook, merge_notebooks


def get_users(filename):

    with open(filename) as f:
        users = [line.strip().split()[0] for line in f]

    return users


def convert_single(user, week, ndigits=None):

    if ndigits is None:
        ndigits = 5

    h = hashlib.sha256()
    h.update(user.encode())
    h.update(str(week).encode())
    hash_str = h.hexdigest()
    hash_int = int(hash_str, 16)

    name = get_random_name(hash_int, hash_int)

    return '{}_{}'.format(name, hash_str[:ndigits])


def make_table(users, week, ndigits=None):

    table = {
        user: convert_single(user, week, ndigits=ndigits) for user in users
    }

    return table


def assign_peers(table, npeers=5):

    names = sorted(table.values())
    wrapped = names * 2

    peers = {}
    for user in table.keys():
        idx = names.index(table[user])
        peers[user] = wrapped[idx:idx + npeers]

    return peers


def assign_notebooks(users, assignment, week):

    release_dir = os.path.join("release", assignment)

    table = make_table(users, week)

    if not os.path.exists(release_dir):
        os.makedirs(release_dir)

    for user in users:

        submitted_dir = os.path.join(
            "submitted", user, "week{}".format(week)
        )


        filenames = [
            f for f in os.listdir(submitted_dir)
            if f.endswith("ipynb")
        ]

        release_user_dir = os.path.join(release_dir, user)
        if not os.path.exists(release_user_dir):
            os.makedirs(release_user_dir)

        peers = assign_peers(table)

        for peer in peers[user]:
            for fname in filenames:
                merged = merge_notebooks(
                    ['peer-assessment/tests/data/header.ipynb', 
                    os.path.join(submitted_dir, fname), 
                    'peer-assessment/tests/data/footer.ipynb']
                )
                write_path = os.path.join(
                    release_user_dir,
                    "{}_by_{}.ipynb".format(fname.split('.')[0], peer)
                )
                write_notebook(write_path, merged)
