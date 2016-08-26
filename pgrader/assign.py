import hashlib
from pgrader.names_generator import get_random_name


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
