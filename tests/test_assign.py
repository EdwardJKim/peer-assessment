import sys
from nose.tools import assert_equal

from pgrader.assign import make_table
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

    do_weeks_from_student_list('tests/studentlist.accy')
    do_weeks_from_student_list('tests/studentlist.info490')
