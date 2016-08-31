import os
import sys
import glob
import dateutil.parser
import six
import shutil
from collections import defaultdict


def get_users(filename):

    with open(filename) as f:
        users = [line.strip().split()[0] for line in f]

    return users


def path_to_record(filename):

    # Only split twice on +, giving three components. This allows usernames with +.
    filename_list = filename.rsplit('+', 2)
    if len(filename_list) != 3:
        sys.stderr.write("Invalid filename: {}".format(filename))
        raise 
    username = filename_list[0]
    timestamp = parse_utc(filename_list[2])
    return {'username': username, 'filename': filename, 'timestamp': timestamp}


def groupby(l, key=lambda x: x):
    d = defaultdict(list)
    for item in l:
        d[key(item)].append(item)
    return d


def sort_by_timestamp(records):
    return sorted(records, key=lambda item: item['timestamp'], reverse=True)


def parse_utc(ts):
    """Parses a timestamp into datetime format, converting it to UTC if necessary."""
    if ts is None:
        return None
    if isinstance(ts, six.string_types):
        ts = dateutil.parser.parse(ts)
    if ts.tzinfo is not None:
        ts = (ts - ts.utcoffset()).replace(tzinfo=None)
    return ts


def init_src(exchange_dir, student_id, course_id, assignment_id):

    course_path = os.path.join(exchange_dir, student_id, course_id)
    inbound_path = os.path.join(course_path, 'inbound')

    pattern = os.path.join(inbound_path, '{}+{}+*'.format('data_scientist', assignment_id))
    records = [path_to_record(f) for f in glob.glob(pattern)]
    usergroups = groupby(records, lambda item: item['username'])
    src_records = [sort_by_timestamp(v)[0] for v in usergroups.values()]

    return src_records


def do_copy(src, dest, perms=None):
    """Copy the src dir to the dest dir"""
    shutil.copytree(src, dest)
    if perms:
        for dirname, dirnames, filenames in os.walk(dest):
            for filename in filenames:
                os.chmod(os.path.join(dirname, filename), perms)


def fetch_notebooks(exchange_dir, dest_dir, student_id, course_id, assignment_id):

    course_path = os.path.join(exchange_dir, student_id, course_id)
    inbound_path = os.path.join(course_path, 'inbound')
    src_records = init_src(exchange_dir, student_id, course_id, assignment_id)

    for rec in self.src_records:
        student_id = rec['username']
        src_path = os.path.join(self.inbound_path, rec['filename'])
        dest_path = self._format_path(self.submitted_directory, student_id, self.assignment_id)
        if not os.path.exists(os.path.dirname(dest_path)):
            os.makedirs(os.path.dirname(dest_path))

    dest_path = os.path.join(dest_dir, student_id, assignment_id)

    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))

    sys.stdout.write("Updating submission: {} {}".format(student_id, assignment_id))
    do_copy(src_path, dest_path)

