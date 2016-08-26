from pgrader.assign import make_anonymous
from pgrader.names_generator import get_random_name
from pgrader.file import get_users
from nose.tools import assert_equal


def test_make_anonymous():

    users = get_users("tests/users.yml")
    names = make_anonymous(users)
    assert_equal(len(set(names.keys())), len(users))

    users = [str(i) for i in range(1000)]
    names = make_anonymous(users)
    assert_equal(len(set(names.keys())), 1000)
