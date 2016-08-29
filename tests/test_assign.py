import sys
from nose.tools import assert_equal, assert_not_in

from pgrader.assign import make_table, assign_peers
from pgrader.names_generator import get_random_name


def test_create_table():

    def do_weeks_from_student_list(filename, nweeks=15):

        with open(filename) as f:
            users = [line.strip().split()[0] for line in f]
    
        for week in range(nweeks):
            names = make_table(users, week)
            assert_equal(len(names.keys()), len(users))
            assert_equal(set(names.keys()), set(users))
            assert_equal(len(set(names.values())), len(users))

        sys.stdout.write('{} users.'.format(len(users)))

    do_weeks_from_student_list('tests/data/studentlist.accy')
    do_weeks_from_student_list('tests/data/studentlist.info490')


def test_assign_peers():

    def check_ten_students(table, peers, npeers):
        for peer in table:
            assert_equal(len(peers[peer]), npeers)
            assert_equal(
                set(peers[peer]),
                set([i % 10 for i in
                    range(table[peer] + 1, table[peer] + 1 + npeers)])
            )
            assert_not_in(table[peer], peers[peer])

    table = {
        'a': 0,
        'b': 2,
        'c': 1,
        'd': 9,
        'e': 8,
        'f': 3,
        'g': 6,
        'h': 7,
        'i': 4,
        'j': 5
    }
    peers = assign_peers(table)
    check_ten_students(table, peers, 5)
