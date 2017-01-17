from functionrefactor.parser import Parser
from tests.common_functions import *


def test_namespace():
    ''' ignores_new lines '''
    _in = [
        "namespace Nutella", "{", "}", "namespace PeanutButter{", "}",
        "namespace Cereal{ //something", "}"
    ]

    expected_result_hpp = [
        "namespace Nutella {}// namespace Nutella",
        "namespace PeanutButter {}// namespace PeanutButter",
        "namespace Cereal {//something}// namespace Cereal"
    ]
    expected_result_cpp = [
        "namespace Nutella {}// namespace Nutella",
        "namespace PeanutButter {}// namespace PeanutButter",
        "namespace Cereal {}// namespace Cereal"
    ]

    parser = Parser()
    parse_batch_run(_in, expected_result_hpp, expected_result_cpp,
                    lambda i, txt, h: parser._parse_namespace_block(i, txt, h))


def test_class():
    ''' ignores_new lines '''
    _in = [
        "class Nutella", "{", "};", "class PeanutButter{", "};",
        "class PeanutButter{//something", "};"
    ]

    expected_result_hpp = [
        "class Nutella {}; ", "class PeanutButter {}; ",
        "class PeanutButter {//something}; "
    ]

    expected_result_cpp = ["", "", ""]

    parser = Parser()
    parse_batch_run(_in, expected_result_hpp, expected_result_cpp,
                    lambda i, txt, h: parser._parse_class_block(i, txt, h))
