#
# Copyright 2022-present Linaro Limited
#
# SPDX-License-Identifier: MIT


import pytest
from unittest.mock import MagicMock
from tuxtrigger import yamlload

from tuxtrigger.inputvalidation import YamlValidator
from tuxtrigger.yamlload import (
    yaml_file_read,
    yaml_file_write,
    compare_sha,
)
from pathlib import Path

BASE = (Path(__file__) / "..").resolve()

ERROR_PATH = BASE / "./test_files/error_path.yaml"
HAPPY_PATH = BASE / "./test_files/happy_path.yaml"
FILE_TO_CREATE = BASE / "./test_files/new_file.yaml"

VALUE_DICT = {
    "linux-5.18.y": {
        "sha": "2437f53721bcd154d50224acee23e7dbb8d8c622",
        "ref": "refs/heads/linux-5.18.y",
    }
}
VALUE = "linux-5.18.y"
RIGHT_KEY = "https://gitlab.com/Linaro/lkft/mirrors/stable/linux-stable"
WRONG_KEY = "/linux-not-existing"


def test_yaml_file_read():
    assert type(yaml_file_read(ERROR_PATH)) == dict


def test_create_repo_list(repo_setup_good):
    assert isinstance(next(repo_setup_good), YamlValidator) is True
    assert repo_setup_good is not None


def test_yaml_file_write(tmpdir):
    test_input = yaml_file_read(ERROR_PATH)
    yaml_file_write(test_input, (tmpdir / "test.yaml"))
    assert (tmpdir / "test.yaml").exists()


# def test_find_in_yaml(correct_archive_read, wrong_archive_read):
#     assert {
#         "ref": "refs/heads/linux-5.18.y",
#         "sha": "2437f53721bcd154d50224acee23e7dbb8d8c62b",
#     } == find_in_yaml(VALUE, correct_archive_read)
#     assert find_in_yaml(VALUE, wrong_archive_read) is None


def test_compare_sha_correct(correct_archive_read):
    with pytest.raises(KeyError):
        compare_sha(WRONG_KEY, VALUE, VALUE_DICT, correct_archive_read)
    assert compare_sha(RIGHT_KEY, VALUE, VALUE_DICT, correct_archive_read) is True


def test_compare_sha_wrong(wrong_archive_read):
    assert compare_sha(WRONG_KEY, VALUE, VALUE_DICT, wrong_archive_read) is False
    assert compare_sha(RIGHT_KEY, VALUE, VALUE_DICT, wrong_archive_read) is False


def test_run_lsremote():
    yamlload.run_lsremote = MagicMock(
        return_value={"master": {"ref": "123", "sha": "456"}}
    )
    assert yamlload.run_lsremote(
        "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git", "master"
    ) == {"master": {"ref": "123", "sha": "456"}}
