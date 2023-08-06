#
# Copyright 2022-present Linaro Limited
#
# SPDX-License-Identifier: MIT

import sys
import pytest

from pathlib import Path
import tuxtrigger.__main__ as main_module

BASE = (Path(__file__) / "../..").resolve()

VALUE_DICT = {
    "master": {"sha": "12345", "ref": "refs/master/torvalds"},
    "linux-5.18.y": {"sha": "12345", "ref": "refs/v5.19"},
    "queue/5.4": {"sha": "12345", "ref": "refs/for-laurent"},
}

UID = "2CCI3BkwKdqM4wOOwB5xRRxvOha"

JSON_OUTPUT = {
    "empty": "no_real_values",
    "uid": "1234",
    "git_repo": "https://gitlab.com/no_real_repo",
    "git_ref": "master",
    "git_describe": "v5.19-rc7",
}


@pytest.fixture
def argv():
    return ["tuxtrigger"]


@pytest.fixture(autouse=True)
def patch_argv(monkeypatch, argv):
    monkeypatch.setattr(sys, "argv", argv)


class TestMain:
    def test_start(self, monkeypatch, mocker):
        monkeypatch.setattr(main_module, "__name__", "__main__")
        main = mocker.patch("tuxtrigger.__main__.main", return_value=1)
        exit = mocker.patch("sys.exit")
        main_module.start()
        main.assert_called()
        exit.assert_called_with(1)

    def test_main_version(self, argv, capsys):
        argv.append("-v")
        with pytest.raises(SystemExit):
            main_module.main()
        out, out_err = capsys.readouterr()
        assert "TuxTrigger" in out

    def test_main_correct_data(self, argv, monkeypatch, mocker):
        argv.extend([f"{BASE}/test/test_files/happy_path.yaml"])
        monkeypatch.setattr(main_module, "__name__", "__main__")
        main_lsremote = mocker.patch(
            "tuxtrigger.__main__.run_lsremote", return_value=VALUE_DICT
        )
        main_build_uid = mocker.patch(
            "tuxtrigger.__main__.tux_console_build", return_value=UID
        )
        main_build_output = mocker.patch(
            "tuxtrigger.__main__.build_result", return_value=JSON_OUTPUT
        )
        main_compare_sha = mocker.patch(
            "tuxtrigger.__main__.compare_sha", return_value=True
        )
        exit = mocker.patch("sys.exit")
        main_module.start()
        main_lsremote.assert_called()
        main_build_uid.assert_called()
        main_compare_sha.assert_called()
        main_build_output.assert_called()
        exit.assert_called_with(0)

    def test_main_key_error(self, argv):
        argv.extend([f"{BASE}/test/test_files/error_path.yaml"])
        with pytest.raises(KeyError):
            main_module.main()
            assert main_module.main() == 1

    def test_main_build_never(self, argv, capsys, monkeypatch, mocker):
        argv.append(f"{BASE}/test/test_files/happy_path.yaml")
        monkeypatch.setattr(main_module, "__name__", "__main__")
        main = mocker.patch("tuxtrigger.__main__.run_lsremote", return_value=VALUE_DICT)
        argv.append("--submit=never")
        main_module.main()
        out, out_err = capsys.readouterr()
        main.assert_called()
        assert "** Builds suspended **" in out

    def test_main_build_always(self, argv, capsys, mocker, monkeypatch):
        argv.append(f"{BASE}/test/test_files/happy_path.yaml")
        argv.append("--submit=always")
        monkeypatch.setattr(main_module, "__name__", "__main__")
        main_lsremote = mocker.patch(
            "tuxtrigger.__main__.run_lsremote", return_value=VALUE_DICT
        )
        main_build_uid = mocker.patch(
            "tuxtrigger.__main__.tux_console_build", return_value=UID
        )
        main_build_output = mocker.patch(
            "tuxtrigger.__main__.build_result", return_value=JSON_OUTPUT
        )
        main_module.main()
        main_lsremote.assert_called()
        main_build_uid.assert_called()
        main_build_output.assert_called()
        out, out_err = capsys.readouterr()
        assert "** Submiting Plan for" in out
