# Peer assessment tool for Jupyterhub

Developed for [jupyterhub-info490](https://github.com/EdwardJKim/jupyterhub-info490) and [jupyterhub-accounting](https://github.com/EdwardJKim/jupyterhub-accounting).

## Installation

```shell
$ git clone https://github.com/edwardjkim/peer-assessment
$ cd peer-assessment
$ sudo python3 setup.py install
```

## Fetch

`pgrader` makes a few assumptions about how your assignment files are
organized.
If you use [nbgrader](http://nbgrader.readthedocs.io/) with
[JupyterHub setup for INFO490](https://github.com/EdwardJKim/jupyterhub-info490),
the assignments will be organized with the following directory structure:

```
exchange/{student_id}/{course_id}/inbound/{assignment_id}/{notebook_id}.ipynb
```

So, create a sub-directory named `exchange` where `pgrader` will be run. Copy
the submissiosn, keeping this directory structure.

You also need the source files in the `source/{course_id}/{assignment_id}/`
directory of the pgrader hierarchy. The source files are used when there is no
submission.

When you have everyting in `exchange` and `source`, run `pgrader fetch`.
For example,

```shell
$ pgrader fetch info490-fa16 Week1_Assignment
```

## Assign

Create a `header.ipynb` and a `footer.ipynb`. Examples are in the `tools`
directory. Save them in the current directory (where `pgrader` will be run).
You also need the `rubric.py`. Create peer assessments with `peer assign`.
For example,

```shell
$ pgrader assign Week1_Assignment 1
```

This will create the peer assessment forms in the `release` directory.

## Peer Grading

Students receive a certain amount of points for simply grading their peer's assignments.
Fetch the submissions again with `pgrader fetch`. For example,

```shell
$ pgrader fetch info490-fa16 Week1_Peer_Reviews
```

Running `pgrader given` will write the peer grading scores to stdout.

```shell
$ pgrader given Week1_Peer_Reviews > Week1_Peer_Grading.csv
```

## Peer Assessments

Each student has five assignments to grade as part of peer assessment. We drop
the highest and lowest score and average the three remaining scores.

```shell
$ pgrader received Week1_Peer_Reviews 1 > Week1_Peer_Assessments.csv
```

## Comments

`pgrader comments` writes the comments in the YAML format.


```shell
$ pgrader comments Week1_Peer_Reviews 1 > Week1_Comments.yml
```
