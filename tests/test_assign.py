from pgrader.assign import convert_single
from pgrader.names_generator import get_random_name
from pgrader.file import get_users
from nose.tools import assert_equal


def test_convert_single():

    users = get_users("tests/users.yml")
    names = [convert_single(user, 1) for user in users]
    assert_equal(len(names), len(users))
        
