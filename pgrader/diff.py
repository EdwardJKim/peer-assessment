import os
import sys
from collections import defaultdict
from difflib import Differ, SequenceMatcher
from pgrader.merge import read_notebook


def extract_source(filename):

    result = {}
    nb = read_notebook(filename)
    for cell in nb.cells:
        metadata = cell['metadata']
        if 'nbgrader' in metadata and metadata['nbgrader']['solution']:
            grade_id = metadata['nbgrader']['grade_id']
            result[grade_id] = cell['source'].split('\n')
    return result


def extract_solution_diff(source, solution):

    delta = []
    for grade_id in sorted(source.iterkeys()):
        #diff = d.compare(source[grade_id], solution[grade_id])
        #delta = ' '.join(i[2:] for i in diff if i.startswith('+ '))
        delta += [s.strip() for s in solution[grade_id] if s not in source[grade_id]]
        #result[grade_id] = delta

    delta = ' '.join(delta)
    return delta


def get_src_path(course_id, assignment_id):

    return os.path.join("source", course_id, assignment_id)


def get_sol_path(user, assignment_id):

    return os.path.join("submitted", user, assignment_id)


def get_notebook_names(course_id, assignment_id):

    src_path = get_src_path(course_id, assignment_id)
    notebooks = [i for i in os.listdir(src_path) if i.endswith('ipynb')]
    return notebooks


def get_solutions(users, course_id, assignment_id):

    src_path = get_src_path(course_id, assignment_id)
    notebooks = get_notebook_names(course_id, assignment_id)

    result = defaultdict(str)
    for user in users:
        for notebook in notebooks:
            sol_path = get_sol_path(user, assignment_id)
            src = extract_source(os.path.join(src_path, notebook))
            sol = extract_source(os.path.join(sol_path, notebook))
            result[user] += extract_solution_diff(src, sol)

    return result


def compare_notebooks(users, course_id, assignment_id, min_ratio=0.8):

    result = []
    solutions = get_solutions(users, course_id, assignment_id)

    for i, user in enumerate(sorted(users)):

        peers = sorted(users) # make a copy

        for peer in peers[i+1:]:
            if solutions[user] and solutions[peer]:

                set_user = set(solutions[user].split())
                set_peer = set(solutions[peer].split())
                len_intersect = len(set_user.intersection(set_peer))
                intersect_score = float(len_intersect) / min(len(set_user), len(set_peer))

                matcher = SequenceMatcher(None, solutions[user], solutions[peer])
                diff_score = matcher.ratio()

                score = max(intersect_score, diff_score)

                if score > min_ratio:
                    result.append((user, peer, score))

    result = sorted(result, key=lambda x: x[2], reverse=True)

    return result
