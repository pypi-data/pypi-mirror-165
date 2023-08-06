#
# Copyright 2022-present Linaro Limited
#
# SPDX-License-Identifier: MIT

from tuxtrigger.exceptions import InvalidArgument, TuxTriggerException


def test_tux_trig_exception():
    exc = TuxTriggerException()
    assert isinstance(exc, Exception) is True


def test_invalid_args():
    arg_exc = InvalidArgument()
    assert isinstance(arg_exc, TuxTriggerException) is True
