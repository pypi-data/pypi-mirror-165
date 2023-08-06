# Copyright (C) 2022 Panther Labs Inc
#
# Panther Enterprise is licensed under the terms of a commercial license available from
# Panther Labs Inc ("Panther Commercial License") by contacting contact@runpanther.com.
# All use, distribution, and/or modification of this software, whether commercial or non-commercial,
# falls under the Panther Commercial License to the extent it is permitted.

# coding=utf-8
# *** WARNING: generated file
import ast
import typing
import unittest
import inspect

from panther_core import PantherEvent
from . import detection, _utilities

__all__ = ["PantherPythonFilterTestCase"]


class PantherPythonFilterTestCase(unittest.TestCase):
    @staticmethod
    def _parseFilterFunc(pfilter: detection.PythonFilter) -> typing.Any:
        func_src = _utilities.snapshot_func(pfilter.func)
        sourcefile = inspect.getsourcefile(pfilter.func) or ""
        root_ast = ast.parse(func_src, filename=sourcefile, mode="exec")

        ns = dict(typing=typing)
        exec(ast.unparse(root_ast), ns)
        func: typing.Callable[..., bool] = ns[pfilter.func.__name__]  # type: ignore
        return func

    def _callParsedFilterFunc(
        self, pfilter: detection.PythonFilter, evt: PantherEvent
    ) -> typing.Any:
        func = self._parseFilterFunc(pfilter)
        return func(evt)

    def assertFilterIsValid(self, test_filter: detection.PythonFilter) -> None:
        self.assertIsInstance(
            test_filter,
            detection.PythonFilter,
            "filter is not an instance of PythonFilter",
        )

        try:
            func = self._parseFilterFunc(test_filter)
        except BaseException as err:
            self.fail(f"unable to parse func value: {err}")

        self.assertTrue(callable(func), "parsed filter is not callable")

    def assertFilterMatches(
        self, test_filter: detection.PythonFilter, obj: typing.Any
    ) -> None:
        evt = PantherEvent(obj, data_model=None)
        unparsed_result = test_filter.func(evt)
        self.assertTrue(unparsed_result)

        parsed_result = self._callParsedFilterFunc(test_filter, evt)
        self.assertEqual(
            unparsed_result,
            parsed_result,
            "result from parsed version of filter does not match unparsed result",
        )

    def assertFilterNotMatches(
        self, test_filter: detection.PythonFilter, obj: typing.Any
    ) -> None:
        evt = PantherEvent(obj, data_model=None)
        unparsed_result = test_filter.func(evt)
        self.assertFalse(unparsed_result)

        parsed_result = self._callParsedFilterFunc(test_filter, evt)
        self.assertEqual(
            unparsed_result,
            parsed_result,
            "result from parsed version of filter does not match unparsed result",
        )
