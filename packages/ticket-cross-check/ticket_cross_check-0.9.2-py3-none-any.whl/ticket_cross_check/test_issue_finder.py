from pathlib import Path

import pytest as pytest

from ticket_cross_check.issue_finder import scan_files, ignore_file, line_matcher
from ticket_cross_check.models import IssueFileMatch


def get_absolute_sample_dir():
    SAMPLE_DIR = 'sample_data'
    dir_above_this = Path(__file__).parent.parent.absolute()
    sample_dir = dir_above_this.joinpath(SAMPLE_DIR)
    assert '/sample_data' in str(sample_dir)
    return sample_dir


def test_issue_finder_resources(capsys):
    sample_dir = get_absolute_sample_dir()
    issue_dict = scan_files(sample_dir)
    assert isinstance(issue_dict, dict)
    assert {1, 2, 3, 9999, 88888, 66666} == set(issue_dict.keys())
    assert 5 == len(issue_dict[1])
    assert IssueFileMatch(
        iid=9999,
        filename=str(sample_dir.joinpath('doc/readme.md')),
        line_nr=14,
        matched_issue=None
    ) == issue_dict[9999][0]


def test_ignore_all_dirs(capsys):
    sample_dir = get_absolute_sample_dir()
    result = scan_files(sample_dir, exclude_dirs=['doc', 'spec', 'src'])
    assert 0 == len(result)


def test_ignore_file():
    abs_file = 'application/javascript/services/cwb-ng/src/sass/themes/dark/_variables.scss'
    assert ignore_file(abs_file)


@pytest.mark.parametrize("line", [
    "<foo bar='#123'>",
    """<path d="9.20454545 Z" id="Shape" fill="#4285F4"></path>""",
    """"#123 """
])
def test_line_matcher_nomatch(line):
    assert not line_matcher(line)


@pytest.mark.parametrize("line,match", [
    ("#1234", "1234"),
    (" #123 ", "123"),
    ("# blabla nbla #12345", "12345"),
    ("# blabla nbla #12345 bla foo", "12345")
])
def test_line_matcher_match(line, match):
    matches = line_matcher(line)
    # assert len(matches) == 1
    assert matches == [match]
