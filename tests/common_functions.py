from functionrefactor.header import *
from functionrefactor.formatter import Formatter
from functionrefactor.string_utilities import find_and_replace_all, is_invalid
import difflib
import sys


def is_strictly_equal(actual, expected):
    assert actual == expected
    if actual == expected:
        print("OK! a: " + actual)
    else:
        print("missmatch:'" + actual + "' not equal to '" + expected + "'")


def remove_whitespace(a):
    return find_and_replace_all(a, '', '\t', '\n', ' ')


def is_equal(actual, expected):

    actual = remove_whitespace(actual).strip()
    expected = remove_whitespace(expected).strip()

    if actual == expected:
        print("OK! a: " + actual)
    else:
        print("missmatch:'" + actual + "' not equal to '" + expected + "'")
    assert actual == expected


def strict_parse_batch_run(input_list, expected_output_hpp,
                           expected_output_cpp, _lamda):

    it = enumerate(input_list)
    txt = next(it)[1]
    result_hpp = []
    result_cpp = []
    while True:
        try:
            h = HeaderDef()
            pos = _lamda(it, txt, h)
            result_hpp.append(h.format_hpp())
            result_cpp.append(h.format_cpp())
            txt = next(it)[1]
        except StopIteration:
            break
    are_equal(result_hpp, expected_output_hpp)
    are_equal(result_cpp, expected_output_cpp)


def parse_batch_run(input_list, expected_output_hpp, expected_output_cpp,
                    _lamda):

    it = enumerate(input_list)
    txt = next(it)[1]
    result_hpp = []
    result_cpp = []
    while True:
        try:
            h = HeaderDef()
            pos = _lamda(it, txt, h)
            result_hpp.append(h.format_hpp())
            result_cpp.append(h.format_cpp())
            txt = next(it)[1]
        except StopIteration:
            break

    are_equal(result_hpp, expected_output_hpp)
    are_equal(result_cpp, expected_output_cpp)


def are_equal(list_actual, list_exp):
    #removes empty lines
    list_actual = [x for x in list_actual if not is_invalid(x)]
    list_exp = [x for x in list_exp if not is_invalid(x)]

    '''ignores spaces tabs and newlines, on the basis that test errors are too frequent to be of any use.
        spaces can be easily added when needed from the header.py and header_components.py classes'''
    diff = difflib.SequenceMatcher(lambda x: x in ['\t', ' ', '\n'],
                                   list_actual, list_exp, True)
    diff_ratio = diff.ratio()
    if diff_ratio < 0.99:
        print("Missmatch: diff_ratio: %s " % diff_ratio)
        sys.stdout.writelines(
            difflib.unified_diff(list_actual, list_exp, 'result', 'expected'))
    else:
        return

    for a, b in zip(list_actual, list_exp):
        is_equal(a, b)


def are_strictly_equal(list_actual, list_exp):
    for a, b in zip(list_actual, list_exp):
        is_strictly_equal(a, b)

    if len(list_actual) != len(list_exp):
        print("missmatch_between actual and expected")
        print(list_actual)
        print(list_exp)

    assert len(list_actual) == len(list_exp)


def full_regex_match(str, regex):
    ''' looks if the full match equals to the input string'''
    assert regex.match(str).group(0) == str


def full_regex_search(str, regex, result_str):
    ''' looks if the full search equals to the result_str'''
    assert regex.search(str).group(0) == result_str
