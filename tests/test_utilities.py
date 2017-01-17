from functionrefactor.string_utilities import *
from tests.common_functions import *
import re


def test():
    assert first_word(
        'ultimate answer is 42, although the question is unclear') == 'ultimate'

    assert first_word('!ultimate answer is 42, although the question is unclear'
                     ) == '!ultimate'

    assert nth_word('ultimate answer is 42, although the question is unclear',
                    4) == '42,'
    assert nth_word('ultimate answer is 42, although the question is unclear',
                    9) == 'unclear'

    assert find_and_replace(
        'int test_variable = 0; //test ', '',
        re.compile(r'\/\/.+')).strip() == 'int test_variable = 0;'

    assert find_and_replace_once(' test string 0 1 2 3 4', '', '0',
                                 '1') == ' test string   2 3 4'

    assert find_and_replace_once('test string 4 2 4 2 4 2', '', '2',
                                 '4') == 'test string   4 2 4 2'

    assert find_and_replace_all('test string 4 2 4 2 4 2', '', '2',
                                '4') == 'test string      '

    assert find_and_replace_all('test', '', 'test', '4') == ''
