from functionrefactor.commands import launch_case
from functionrefactor.formatter import Formatter
from functionrefactor.settings import *
from tests.common_functions import *

import json


class TestRuns():
    def test_runs(self):
        with open("tests/cases/test_cases.json", "r") as tcf:
            test_launcher = json.load(tcf)

        settings.update_global_settings(test_launcher)
        test_cases = test_launcher["launcher"]

        for case in test_cases:
            if case["active"]:
                [hpp_result, cpp_result] = launch_case("tests/cases",case)
                self.check_result("tests/cases/" + case["hpp_out"],
                                  "tests/cases/" + case["cpp_out"], hpp_result,
                                  cpp_result)

    def check_result(self, hpp_path, cpp_path, hpp_result, cpp_result):

        clang_formatter = Formatter()
        hpp_expected_result = clang_formatter.open_and_launch(hpp_path)
        cpp_expected_result = clang_formatter.open_and_launch(cpp_path)

        are_equal(hpp_result, hpp_expected_result)
        are_equal(cpp_result, cpp_expected_result)
