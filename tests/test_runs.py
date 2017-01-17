from functionrefactor.commands import parse_header, parse_to_file
from functionrefactor.formatter import Formatter
from tests.common_functions import *

import json


class TestRuns():
    def test_runs(self):
        with open("tests/cases/test_cases.json", "r") as tcf:
            json_file = json.load(tcf)

        test_cases = json_file['cases_to_run']
        overwrite = False

        for case in test_cases:
            if test_cases[case]:
                self.read_case_input(case, overwrite)

    def read_case_input(self, case_name, overwrite):
        path = "tests/cases/" + case_name
        input_path = path + "_in.hpp"
        out_hpp_path = path + ".hpp"
        out_cpp_path = path + ".cpp"

        if overwrite:
            parse_to_file(input_path, out_hpp_path, out_cpp_path)
            return

        print("launching test case at: " + input_path)
        [hpp_result, cpp_result] = parse_header(input_path)
        clang_formatter = Formatter()
        hpp_expected_result = clang_formatter.open_and_launch(out_hpp_path)
        cpp_expected_result = clang_formatter.open_and_launch(out_cpp_path)

        are_equal(hpp_result, hpp_expected_result)
        are_equal(cpp_result, cpp_expected_result)
