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


def assign_peers(table, npeers=5, shuffle=True):

    names = sorted(table.keys())
    if shuffle:
        random.shuffle(names)
    wrapped = names * 2

    peers = {}
    for idx, name in enumerate(names):
        peers[name] = wrapped[idx + 1: idx + 1 + npeers]

    return peers


def assign_notebooks(users, assignment_id, week,
    header="header.ipynb", footer="footer.ipynb", remove_header=False):

    release_dir = os.path.join("release", assignment_id)

    table = make_table(users, week)

    if not os.path.exists(release_dir):
        os.makedirs(release_dir)

    peers = assign_peers(table)

    for user in users:

        submitted_dir = os.path.join("submitted", user, assignment_id)

        filenames = [
            f for f in os.listdir(submitted_dir)
            if f.endswith("ipynb") and f.startswith("Problem_")
        ]

        release_user_dir = os.path.join(release_dir, user)
        if not os.path.exists(release_user_dir):
            os.makedirs(release_user_dir)

        for peer in peers[user]:
            for fname in filenames:

                peer_path = os.path.join(
                    "submitted", peer, assignment_id, fname
                )
                merged = merge_notebooks(
                    [header, peer_path, footer],
                    remove_header=remove_header
                )
                write_path = os.path.join(
                    release_user_dir,
                    "{}_{}.ipynb".format(fname.split('.')[0], table[peer])
                )
                write_notebook(write_path, merged)

        shutil.copy("rubric.py", os.path.join(release_user_dir, "rubric.py"))
