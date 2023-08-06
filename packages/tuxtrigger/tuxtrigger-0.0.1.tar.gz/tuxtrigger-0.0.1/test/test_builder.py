#
# Copyright 2022-present Linaro Limited
#
# SPDX-License-Identifier: MIT

from unittest.mock import MagicMock
import pytest

from pathlib import Path
from tuxtrigger import builder
from tuxtrigger.builder import (
    squad_submit,
    tux_console_build,
    tux_console_plan,
    build_result,
)

PARAMS = {
    "git_repo": "https://gitlab.com/Linaro/lkft/mirrors/stable/linux-stable-rc",
    "git_ref": "master",
    "target_arch": "x86_64",
    "toolchain": "gcc-12",
    "kconfig": "tinyconfig",
}

FAIL_PARAMS = {
    "git_repo": "https://gitlab.com/not_existing_repo",
    "git_ref": "not_existing_branch",
    "target_arch": "x86_64",
    "toolchain": "gcc-12",
    "kconfig": "tinyconfig",
}

BASE = (Path(__file__) / "..").resolve()

PLAN = BASE / "test_files/planTest.yaml"
PLAN_FAIL = BASE / "test_files/planTestc.yaml"
JSON_PLAN_RESULT = BASE / "test_files/plan_result.json"

UID = "2CCI3BkwKdqM4wOOwB5xRRxvOha"


def test_tux_console_build():
    uid_value = tux_console_build(**PARAMS)
    assert uid_value is not None
    assert len(uid_value) == 27


def test_tux_console_build_mock():
    builder.tux_console_build = MagicMock(return_value=UID)
    assert builder.tux_console_build() == UID


def test_tux_console_plan(squad_group_good, squad_project_good):
    json_data = None
    assert tux_console_plan(json_data, PLAN, squad_group_good, squad_project_good) == 1


def test_build_result():
    json_output = build_result(UID)
    assert build_result(None) is None
    assert isinstance(json_output, dict)


def test_build_result_list():
    builder.build_result_list = MagicMock(return_value=0)
    assert builder.build_result_list() == 0


def test_tux_console_build_error(capsys):
    with pytest.raises(Exception):
        fail_build = tux_console_build(**FAIL_PARAMS)
        out, out_err = capsys.readouterr()
        assert fail_build != 0
        assert "Tuxsuite not build" in out


def test_tux_console_plan_error(squad_group_good, squad_project_good):
    json_data = {
        "empty": "no_real_values",
        "uid": "1234",
        "git_repo": "https://gitlab.com/no_real_repo",
        "git_ref": "master",
        "git_describe": "v5.19-rc7",
    }
    fail_plan = tux_console_plan(
        json_data, PLAN_FAIL, squad_group_good, squad_project_good
    )
    assert fail_plan != 0


def test_squad_submit(squad_env_setup, squad_group_good, squad_project_good):
    json_data = {
        "empty": "no_real_values",
        "uid": "1234",
        "git_repo": "https://gitlab.com/no_real_repo",
        "git_ref": "master",
        "git_describe": "v5.19-rc7",
    }
    with pytest.raises(Exception):
        squad_submit(json_data, squad_group_good, squad_project_good, JSON_PLAN_RESULT)
