import os
import sys
import yaml

from pgrader.assign import get_users, make_table


def inverted(table):

    return {value: key for key, value in table.items()}


def get_review(user, assignment_id):

    release_user_dir = os.path.join("submitted", user, assignment_id)

    filename = os.path.join(
        release_user_dir, "{}.yml".format(assignment_id)
    )

    if os.path.exists(filename):
        with open(filename) as f:
            yaml_data = yaml.load(f.read())
    else:
        yaml_data = None

    return yaml_data


def validate_score(score):
    return score >= 0 and score <= 5


def validate_comment(comment):
    # TODO: NLP?
    if comment:
        return True
    else:
        return False


def get_peer_grading_single(user, assignment_id):

     yaml_data = get_review(user, assignment_id)

     score = 0

     if yaml_data:
         for peer in yaml_data:
             review = yaml_data[peer]
             if (validate_score(review["correctness"]) and
                 validate_score(review["readability"])):
                 score += 2
             if validate_comment(review["comments"]):
                 score += 1

     return score


def get_peer_grading(users, assignment_id):

     for user in users:
          score = get_peer_grading_single(user, assignment_id)
          sys.stdout.write("{},{}\n".format(
              user, get_peer_grading_single(user, assignment_id)
          ))


def get_peer_assessment(users, assignment_id, week):

    score = {}

    for user in users:

         yaml_data = get_review(user, assignment_id)

         if yaml_data:

             for problem_peer in yaml_data:

                 problem, peer = problem_peer.split('_', 1)

                 if peer not in score:
                     score[peer] = {}

                 if problem not in score[peer]:
                     score[peer][problem] = []
                 review = yaml_data[problem_peer]

                 if (validate_score(review["correctness"]) and
                     validate_score(review["readability"])):
                     score[peer][problem].append(
                         float(review["correctness"]) +
                         float(review["readability"])
                     )

    table = make_table(users, week)

    result = {}

    for user in users:
        name = table[user]
        if user not in result:
            result[user] = 0
        if name in score:
            for prob in score[name]:
                if len(score[name][prob]) > 0:
                    result[user] += max(score[name][prob])
                else:
                    result[user] = -99999
                    sys.stdout.write("No peer assesment found for {}, {}\n"
                        "".format(user, prob))

    for key, value in result.items():
        sys.stdout.write("{},{}\n".format(key, value))
