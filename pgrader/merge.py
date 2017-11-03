import os
import sys
import io
import nbformat


def read_notebook(filename):

    with io.open(filename, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    return nb


def write_notebook(filename, notebook):

    with io.open(filename, 'w', encoding='utf-8') as f:
        f.write(notebook)


def merge_notebooks(filenames, remove_header=False):
    merged = None
    for fname in filenames:
        nb = read_notebook(fname)
        if remove_header:
            for i, cell in enumerate(nb.cells[:]):
                grade_id_exists = ('nbgrader' in cell['metadata']) and ('grade_id' in cell['metadata']['nbgrader'])
                header_exists = grade_id_exists and (cell['metadata']['nbgrader']['grade_id'] == 'header')
                due_date_exists = grade_id_exists and (cell['metadata']['nbgrader']['grade_id'] == 'due_date')
                if header_exists or due_date_exists:
                    nb.cells.remove(cell)
        if merged is None:
            merged = nb
        else:
            # TODO: add an optional marker between joined notebooks
            # like an horizontal rule, for example, or some other arbitrary
            # (user specified) markdown cell)
            merged.cells.extend(nb.cells)
    if not hasattr(merged.metadata, 'name'):
        merged.metadata.name = ''
    merged.metadata.name += "_merged"
    return nbformat.writes(merged)
