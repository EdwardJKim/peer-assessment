from pgrader.names_generator import get_random_name
from pgrader.file import get_users


def make_anonymous(users, week=1):

    names = {}
    for user in users:
        n = hash(user)
        while True:
            name = get_random_name(n, n - week)
            if name not in names.keys():
                names[name] = user
                break
            else:
                n = n - 1

    return names
