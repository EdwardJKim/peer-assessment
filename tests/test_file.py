from peer_assessment.file import get_users
from nose.tools import assert_equal

def test_jupyterhub_users():
    assert_equal(
        get_users('tests/users.yml'),
        ['alterego0', 'superego0', 'alterego1',
         'superego1', 'alterego2', 'superego2']
        )

