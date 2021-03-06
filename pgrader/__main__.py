import os
import sys
from pgrader.assign import get_users, assign_notebooks
from pgrader.fetch import fetch_notebooks
from pgrader.autograde import get_peer_grading, get_peer_assessment
from pgrader.comments import get_comments
from pgrader.diff import compare_notebooks


def main(args=None):

    if args is None:
        args = sys.argv[1:]

    # check if a file named studentlist exsits.
    # this file should have usernames separated by lines.
    if os.path.exists("studentlist"):
        users = get_users("studentlist")
    else:
        sys.stderr.write(
            "A file named 'studentlist' with the list of usernames must exist.\n"
        )
        return 1

    # check for subcommand
    if len(args) == 0:
        sys.stderr.write(
            "Usage: pgrader <subcommand>\n"
            "Valid subcommands are: fetch, assign, given, received, comments\n"
        )
        return 1

    # fetch subcommand requires course_id and assignment_id
    if args[0] == "fetch":
        if len(args[1:]) != 2:
            sys.stderr.write(
                "Usage: pgrader fetch <course_id> <assignment_id>\n"
            )
            return 1
        course_id = args[1]
        assignment_id = args[2]
        for user in users:
            fetch_notebooks(
                os.path.join(os.getcwd(), "exchange"),
                os.path.join(os.getcwd(), "submitted"),
                user, course_id, assignment_id
            )

    # diff subcommand requires course_id and assignment_id
    if args[0] == "diff":
        if len(args[1:]) != 2:
            sys.stderr.write(
                "Usage: pgrader diff <course_id> <assignment_id>\n"
            )
            return 1
        course_id = args[1]
        assignment_id = args[2]
        diff = compare_notebooks(users, course_id, assignment_id)
        for d in diff:
            sys.stdout.write("{0},{1},{2:.3f}\n".format(*d))

    elif args[0] == "assign":
        # assign subcommand requires assignment_id and week_number
        if len(args[1:]) == 2:
            assignment_id = args[1]
            week_number = args[2]
            nnb_per_week = 3
            nnotebooks = 2 * nnb_per_week
        elif len(args[1:]) == 3:
            assignment_id = args[1]
            week_number = args[2]
            nnb_per_week = int(args[3])
            nnotebooks = 2 * nnb_per_week
        else:
            sys.stderr.write(
                "Usage: pgrader assign <assignment_id> <week_number> <number_of_notebooks>\n\n"
                "number_of_notebooks is optional. (Default: 4)\n"
            )
            return 1
        assign_notebooks(
            users, assignment_id, week_number,
            nnotebooks=nnotebooks, nnb_per_week=nnb_per_week, remove_header=True)

    elif args[0] == "given":
        # autograde subcommand requires assignment_id
        if len(args[1:]) != 1:
            sys.stderr.write("Usage: pgrader given <assignment_id>\n")
            return 1
        assignment_id = args[1]
        get_peer_grading(users, assignment_id)

    elif args[0] == "received":
        # autograde subcommand requires assignment_id and week_number
        if len(args[1:]) != 2:
            sys.stderr.write(
                "Usage: pgrader received <assignment_id> <week_number>\n"
            )
            return 1
        assignment_id = args[1]
        week_number = args[2]
        get_peer_assessment(users, assignment_id, week_number)

    elif args[0] == "comments":
        # autograde subcommand requires assignment_id and week_number
        if len(args[1:]) != 2:
            sys.stderr.write(
                "Usage: pgrader comments <assignment_id> <week_number>\n"
            )
            return 1
        assignment_id = args[1]
        week_number = args[2]
        get_comments(users, assignment_id, week_number)

    else:
        sys.stderr.write(
            "Valid subcommands are: fetch, assign, given, received, comments\n"
        )


if __name__ == "__main__":
    main()

