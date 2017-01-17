from functionrefactor.parser import Parser, TemplateParser, Regex
from tests.common_functions import *


def test_templates():
    ''' ignores_new lines '''
    _in = [
        "template <typename T>", "template <class Name = std::ForwardIterator>",
        "template", "<typename TT, typename U, int X_size = 10>", "template",
        "<typename T=float,", "typename C=long long>", ""
    ]

    expected_result_hpp = [
        "using T = change_this;", "using Name = std::ForwardIterator;",
        "using TT = change_this;\nusing U = change_this;\nconstexpr int X_size = 10;",
        "using T = float;\nusing C = long long;"
    ]

    expected_result_cpp = ["", "", "", ""]
    rg = Regex()
    parser = TemplateParser(rg)
    parse_batch_run(_in, expected_result_hpp, expected_result_cpp,
                    lambda i, pos, h: parser.parse(i, pos, h))


def test_template_parser():
    ''' uses main parse function parse_block which determines what is contained in each line '''
    _in = [
        "template <typename T>", "template <class Name = std::ForwardIterator>",
        "template", "<typename TT, typename U, int X_size = 10>", "template",
        "<typename T=float,", "typename C=long long>", ""
    ]

    expected_result_hpp = [
        "\nusing T = change_this;\n", "using Name = std::ForwardIterator;\n",
        "using TT = change_this;\nusing U = change_this;\nconstexpr int X_size = 10;\n",
        "using T = float;\nusing C = long long;\n"
    ]

    expected_result_cpp = ["", "", "", "", "", "", ""]

    parser = Parser()
    h = HeaderDef()
    it = enumerate(_in)
    pos = next(it)[1]
    try:
        parser.parse_block(it, pos, h)
    except StopIteration:
        pass

    is_equal(h.format_hpp(), ''.join(expected_result_hpp))
    is_equal(h.format_cpp(), "")
