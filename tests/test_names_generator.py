from pgrader import names_generator as ng
from nose.tools import assert_equal

def test_left():
    assert_equal(ng.choose_left(0), "admiring")
    assert_equal(ng.choose_left(1), "adoring")
    assert_equal(ng.choose_left(2), "agitated")
    assert_equal(ng.choose_left(66), "zen")

def test_right():
    assert_equal(ng.choose_right(0), "albattani")
    assert_equal(ng.choose_right(1), "allen")
    assert_equal(ng.choose_right(2), "almeida")
    assert_equal(ng.choose_right(150), "albattani")

def test_get_random_name():
    assert_equal(ng.get_random_name(0, 0), "admiring_albattani")
    assert_equal(ng.get_random_name(0, 1), "admiring_allen")
    assert_equal(ng.get_random_name(1, 0), "adoring_albattani")
    assert_equal(ng.get_random_name(1, 1), "adoring_allen")
