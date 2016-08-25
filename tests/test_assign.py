from peer_assessment.assign import make_anonymous
from peer_assessment.names_generator import get_random_name
from peer_assessment.file import get_users
from nose.tools import assert_equal


def test_make_anonymous():

    users = get_users("tests/users.yml")
    names = make_anonymous(users)
    assert_equal(len(set(names.keys())), len(users))

    users = [str(i) for i in range(1000)]
    names = make_anonymous(users)
    assert_equal(len(set(names.keys())), 1000)
