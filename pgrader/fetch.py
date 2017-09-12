import os
import sys
import glob
import dateutil.parser
import six
import shutil
from collections import defaultdict


def path_to_record(filename):

    # Only split twice on +, giving three components. This allows usernames with +.
    filename_list = filename.rsplit('+', 2)
    if len(filename_list) != 3:
        sys.stderr.write("Invalid filename: {}".format(filename))
        raise 
    timestamp = parse_utc(filename_list[2])
    return {'filename': filename, 'timestamp': timestamp}


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
    for record in records:
        record['username'] = student_id
    usergroups = groupby(records, lambda item: item['username'])
    src_records = [sort_by_timestamp(v)[0] for v in usergroups.values()]

    return src_records


def copy_src_dir(src, dest, perms=None):
    """Copy the src dir to the dest dir"""
    shutil.copytree(src, dest)
    if perms:
        for dirname, dirnames, filenames in os.walk(dest):
            for filename in filenames:
                os.chmod(os.path.join(dirname, filename), perms)


def copy_src_file(src, dest, perms=None):
    """Copy the src file to the dest dir"""
    shutil.copy(src, dest)
    if perms:
        for dirname, dirnames, filenames in os.walk(dest):
            for filename in filenames:
                os.chmod(os.path.join(dirname, filename), perms)


def fetch_notebooks(exchange_dir, dest_dir, student_id, course_id, assignment_id):

    course_path = os.path.join(exchange_dir, student_id, course_id)
    inbound_path = os.path.join(course_path, 'inbound')
    source_path = os.path.join('source', course_id, assignment_id)
    src_records = init_src(exchange_dir, student_id, course_id, assignment_id)

    if src_records:
        src_path = os.path.join(inbound_path, src_records[0]['filename'])
    else:
        sys.stdout.write(
            "No submission: {} {}\n".format(student_id, assignment_id)
        )
        src_path = source_path

    dest_path = os.path.join(dest_dir, student_id, assignment_id)
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))

    sys.stdout.write(
        "Copying submission: {} {}\n".format(student_id, assignment_id)
    )
    copy_src_dir(src_path, dest_path)

    src_files = [f for f in os.listdir(source_path)]
    dest_files = [f for f in os.listdir(dest_path)]

    for src_file in src_files:
        if src_file not in dest_files:
            copy_src_file(os.path.join(source_path, src_file), dest_path)

    for dest_file in dest_files:
        if dest_file not in src_files:
            d = os.path.join(dest_path, dest_file)
            if os.path.isfile(d):
                os.remove(d)
            else:
                shutil.rmtree(d)
