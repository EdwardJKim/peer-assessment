from peer_assessment import names_generator as ng
from nose.tools import assert_equal

def test_left():
    assert_equal(ng.choose_left(0), "silly")
    assert_equal(ng.choose_left(1), "boring")

def test_right():
    assert_equal(ng.choose_right(0), "sinoussi")
    assert_equal(ng.choose_right(1), "bose")

def test_get_random_name():
    assert_equal(ng.get_random_name(0, 0), "silly_sinoussi")
    assert_equal(ng.get_random_name(0, 1), "silly_bose")
    assert_equal(ng.get_random_name(1, 0), "boring_sinoussi")
    assert_equal(ng.get_random_name(1, 1), "boring_bose")
