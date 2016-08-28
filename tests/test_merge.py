import json
from nose.tools import assert_equal
from pgrader.merge import merge_notebooks


def test_merge_notebooks():

    header_path = "tests/data/header.ipynb"
    body_path = "tests/data/body_with_header.ipynb"
    footer_path = "tests/data/footer.ipynb"

    merged_str = merge_notebooks([header_path, body_path, footer_path])
    merged = json.loads(merged_str)
    cells = merged['cells']

    assert_equal(cells[0]['source'], ['Header'])
    assert_equal(cells[0]['cell_type'], 'markdown')

    assert_equal(cells[1]['source'], ['Header of body'])
    assert_equal(cells[1]['cell_type'], 'markdown')

    assert_equal(cells[2]['source'], ["print('hello')"])
    assert_equal(cells[2]['cell_type'], 'code')

    assert_equal(cells[3]['source'], ["print('world')"])
    assert_equal(cells[3]['cell_type'], 'code')


def test_remove_header():

    header_path = "tests/data/header.ipynb"
    body_path = "tests/data/body_with_header.ipynb"
    footer_path = "tests/data/footer.ipynb"

    merged_str = merge_notebooks(
        [header_path, body_path, footer_path],
        remove_header=True
    )
    merged = json.loads(merged_str)
    cells = merged['cells']

    assert_equal(cells[0]['source'], ['Header'])
    assert_equal(cells[0]['cell_type'], 'markdown')

    assert_equal(cells[1]['source'], ["print('hello')"])
    assert_equal(cells[1]['cell_type'], 'code')

    assert_equal(cells[2]['source'], ["print('world')"])
    assert_equal(cells[2]['cell_type'], 'code')
