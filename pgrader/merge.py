import os
import sys
import io
import nbformat


def merge_notebooks(filenames, remove_header=False):
    merged = None
    for fname in filenames:
        with io.open(fname, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
        if remove_header:
            for i, cell in enumerate(nb.cells):
                if ('nbgrader' in cell['metadata'] and
                    cell['metadata']['nbgrader']['grade_id'] == 'header'):
                    nb.cells.pop(i)
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
