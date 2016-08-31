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

<<<<<<< HEAD
    def flatten(alist):
        return [i for sublist in alist for i in sublist]

    def check(table, peers, npeers):
        for net_id, docker_name in table.items():
            assigned = peers[net_id]
            assert_equal(len(assigned), npeers)
            assert_not_in(docker_name, peers[net_id])
            assert_equal(
                flatten(list(peers.values())).count(net_id),
                npeers
            )
=======
    def check_ten_students(table, peers, npeers):
        for peer in table:
            assert_equal(len(peers[peer]), npeers)
            assert_equal(
                set(peers[peer]),
                set([i % 10 for i in
                    range(table[peer] + 1, table[peer] + 1 + npeers)])
            )
            assert_not_in(table[peer], peers[peer])
>>>>>>> 5c6915533d45ca4a63c27b7eb6ce9324fe875a31

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
<<<<<<< HEAD
    peers = assign_peers(table, shuffle=False)
    check(table, peers, 5)
    assert_equal(set(peers['a']), set([i for i in 'bcdef']))
    assert_equal(set(peers['b']), set([i for i in 'cdefg']))
    assert_equal(set(peers['c']), set([i for i in 'defgh']))
    assert_equal(set(peers['d']), set([i for i in 'efghi']))
    assert_equal(set(peers['e']), set([i for i in 'fghij']))
    assert_equal(set(peers['f']), set([i for i in 'ghija']))
    assert_equal(set(peers['g']), set([i for i in 'hijab']))
    assert_equal(set(peers['h']), set([i for i in 'ijabc']))
    assert_equal(set(peers['i']), set([i for i in 'jabcd']))
    assert_equal(set(peers['j']), set([i for i in 'abcde']))

    peers = assign_peers(table, shuffle=True)
    check(table, peers, 5)
=======
    peers = assign_peers(table)
    check_ten_students(table, peers, 5)
>>>>>>> 5c6915533d45ca4a63c27b7eb6ce9324fe875a31
