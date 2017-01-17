from functionrefactor.parser import Parser, CommentParser, Regex
from functionrefactor.header import *
from tests.common_functions import *
import pytest


def test_comments():
    ''' ignores_new lines '''
    _in = [
        "//comment is this", "/* comment is this as well */",
        "auto p = get_value(); //some comment",
        "void main(auto& args);/* single line comment */",
        "/* multiline comment", "\n", "\n", "\n", "\n", "\n*/ int i = 0;", ''
    ]

    expected_result = [
        "//comment is this", "/* comment is this as well */", "//some comment",
        '/* single line comment */', "/* multiline comment*/\n"
    ]
    rg = Regex()
    parser = CommentParser(rg)
    parse_batch_run(_in, expected_result, [],
                    lambda i, pos, h: parser.parse(i, pos, h))


def test_comments_strict():
    _in = [
        "auto p = get_value();//some comment",
        "void main(auto& args);/* multi line\n", "comment */",
        "/* multiline comment", "\n", "\n", "\n", "\n", "\n*/ int i = 0;", ''
    ]

    expected_result = [
        "\n//some comment\n",
        '\n/* multi line\ncomment */\n',
        "\n/* multiline comment\n\n\n\n\n*/\n",
    ]
    rg = Regex()
    parser = CommentParser(rg)

    strict_parse_batch_run(_in, expected_result, [],
                           lambda i, pos, h: parser.parse(i, pos, h))


def test_comment_parser():
    ''' uses main parse function parse_block which determines what is contained in each line
    '''
    _in = [
        "//comment is this\n", "/* comment is this as well */\n",
        "    //some comment\n", "/* single line comment */\n",
        "/* multiline comment\n", "\n", "\n", "\n", "\n", "\n*/", ''
    ]
    expected_result = [
        "\n//comment is this\n", "/* comment is this as well */\n",
        "//some comment\n", "/* single line comment */\n",
        "/* multiline comment\n", "\n", "\n", "\n", "\n", "\n*/\n"
    ]

    parser = Parser()
    h = HeaderDef()
    it = enumerate(_in)
    pos = next(it)
    try:
        parser.parse_block(it, pos[1], h)
    except StopIteration:
        pass

    is_equal(h.format_hpp(), ''.join(expected_result))
