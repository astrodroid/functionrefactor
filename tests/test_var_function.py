from functionrefactor.parser import Parser, Regex, FunctionVariableParser
from tests.common_functions import *


def test_variable_capture():

    rg = Regex()
    parser = FunctionVariableParser(rg)

    [keywords, name, rhs] = parser._extract_variable_components('int i;')
    is_equal(''.join([f.format_hpp() for f in keywords]), 'int')
    is_equal(name, 'i')
    is_equal(rhs, ';')

    [keywords, name, rhs] = parser._extract_variable_components(
        'const auto& index = 0;')
    is_equal(''.join([f.format_hpp() for f in keywords]), 'const auto&')
    is_equal(name, 'index')
    is_equal(rhs, '=0;')

    [keywords, name, rhs] = parser._extract_variable_components(
        'const auto& index {0};')
    is_equal(''.join([f.format_hpp() for f in keywords]), 'const auto&')
    is_equal(name, 'index')
    is_equal(rhs, '{0};')

    [keywords, name, rhs] = parser._extract_variable_components(
        r'const std::ForwardIterator<int>* begin{*ptr};')
    is_equal(''.join([f.format_hpp() for f in keywords]),
             r'const std::ForwardIterator<int> *')
    is_equal(name, 'begin')
    is_equal(rhs, '{*ptr};')


def test_variables():
    ''' ignores_new lines '''
    _in = [
        "int i;", "int i = 0;", "int i{0};", "auto i = (0);",
        "std::vector<int> vec {1,2,3,4};", "std::vector<float> vec\n",
        "= { 0.f , 2.f , 4.f , 8.f };"
    ]

    expected_result_hpp = [
        "int i;", "int i= 0;", "int i{0};", "auto i= (0);",
        "std::vector<int> vec{1,2,3,4};",
        "std::vector<float> vec= { 0.f , 2.f , 4.f , 8.f };"
    ]

    expected_result_cpp = ["", "", "", "", "", ""]
    rg = Regex()
    parser = FunctionVariableParser(rg)
    parse_batch_run(_in, expected_result_hpp, expected_result_cpp,
                    lambda i, pos, h: parser.parse(i, pos, h))


def test_functions():
    ''' ignores_new lines '''
    _in = [
        'void func();', 'std::string get_key(int index_pos = 0);',
        'std::string get_key(int index_pos = 0)',
        '{return ptr->find_key(index_pos);\n', '}',
        'std::vector<int> get_vector(int min_number = 0, int max_number = 10);'
    ]

    expected_result_hpp = [
        'void func();', 'std::string get_key(int index_pos= 0);',
        'std::string get_key(int index_pos= 0);',
        'std::vector<int> get_vector(int min_number = 0, int max_number = 10);'
    ]

    expected_result_cpp = [
        'void func() {}', 'std::string get_key(int index_pos) {}',
        'std::string get_key(int index_pos){return ptr->find_key(index_pos);}',
        'std::vector<int> get_vector(int min_number, int max_number) {}'
    ]

    rg = Regex()
    parser = FunctionVariableParser(rg)

    parse_batch_run(_in, expected_result_hpp, expected_result_cpp,
                    lambda i, pos, h: parser.parse(i, pos, h))

    _class = ClassDef("class", "Base")
    _in = ["void do_things(){ do_other_things();}", ""]
    it = enumerate(_in)
    pos = next(it)[1]
    _parser = Parser()
    try:
        _parser.parse_block(it, pos, _class)
    except StopIteration:
        pass

    is_equal(
        _class.format_cpp(None),
        "void  Base::do_things(){ do_other_things();}")
