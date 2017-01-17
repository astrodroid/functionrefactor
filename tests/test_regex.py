from functionrefactor.parser import Regex
from tests.common_functions import *


def test_comment_regex():
    r = Regex()
    assert r.comment_single_line.match("//comment")
    assert r.comment_single_line.match("    //comment something")
    assert r.comment_multiline.match("    /*comment something*/")
    assert r.comment_multiline.match("    /*comment \n something*/")
    assert r.comment_multiline_begin.match(
        "    /*comment \n something \n \n \n \n")
    assert r.comment_multiline_begin.match("    /*c++")
    assert r.comment_multiline_end.match("comment */")
    assert r.comment_multiline_end.match("comment \n something \n */   ")


def test_preprocessor_regex():
    r = Regex()
    assert r.preprocessor_c.match("#define")
    assert r.preprocessor_c.match("#define MACRO_ SOMETHING(){} \ ")

    assert r.includes.match("#include <string>")
    assert r.includes.match("#include \"_header\" ")
    assert r.generic_preprocessor.match("#ifdef SOMETHING")
    assert r.generic_preprocessor.match("#endif //SOMETHING ELSE")

    assert r.line_continuation.match(r"#define MACRO \ ")
    assert r.line_continuation.match(r"return CAPSLOCKMANDATORY; \ ")


def test_class_namespace_regex():
    r = Regex()
    assert r.namespace.match("namespace std \n {")
    assert r.namespace.match("      namespace SuperNamespace{")
    assert r.class_.match("class Nutella{")
    assert not r.class_.match("      class;")
    assert r.class_.match("class Porridge{")
    assert r.struct_.match("struct{")
    assert r.struct_.match("      struct \n \n Cereal{")
    assert r.union_.match(' union Oats{ }')
    assert r.union_.match(' union Variant{ ')


def test_template_arg_packing():
    r = Regex()
    assert r.template.match('  template  typename<>')  # look for template start
    assert r.template.match('  template')  # look for template start
    assert r.template_args.search("template <typename T>")
    assert r.template_args.search(
        "template <class T0, class T1, \n int X = 10 >")

    assert r.template_args.search(
        "template <class T0, class T1, \n int X = 10 > /* */")


def test_text_quotes():
    r = Regex()
    assert r.string_block.search(r" \" something ))) \" ")
    assert r.char_block.search(r" \' c \' ")


def test_variable_and_function_regex():
    r = Regex()
    assert r.is_variable.match("int var;")
    assert r.is_variable.match("auto i{0};")
    assert r.is_variable.match("int i =0;")
    assert r.is_variable.match("auto i{0};")
    assert r.is_variable.match("std::vector<std::string> vec{};")
    assert r.is_variable.match(
        r"std::vector<std::string> vec={\"a\",\"b\",\"c\"}; //abc")
    assert r.is_variable.match(
        r"std::vector<std::string> vec=(\"a\",\"b\",\"c\"); //abc")
    assert r.is_variable.match(r"std::vector<std::string> vec=(\n); //abc")
    assert r.is_variable.match("std::vector<std::string> vec\n{\n}\n;")
    assert r.is_variable.match(
        "constexpr f = [&](auto& a, auto& b)->{return a+b;}")
    assert r.is_variable.match(
        "constexpr f = [&](auto& a, auto& b)->{\n return a+b; \n}")

    assert not r.is_variable.match("int main();")
    assert not r.is_variable.match("int main() { }")
    assert not r.is_variable.match(
        "virtual std::string get_tag(const std::string& key)=0; ")

    # assert r.is_variable.match(r"int i(0); //abc") note this is not a valid variable declaration 
    # in a C++ header file, so no test for this is needed

    full_regex_match("auto i =0;", r.variable_capture)
    full_regex_match("auto i{0};", r.variable_capture)
    full_regex_match("std::vector<std::string> vec{};", r.variable_capture)
    full_regex_match(r"std::vector<std::string> vec={\"a\",\"b\",\"c\"};",
                     r.variable_capture)
    full_regex_match(r"std::vector<std::string> vec=(\"a\",\"b\",\"c\");",
                     r.variable_capture)
    full_regex_match(r"std::vector<std::string> vec=(\n);", r.variable_capture)
    full_regex_match("std::vector<std::string> vec\n{\n}\n;",
                     r.variable_capture)

    #lambda test
    full_regex_match("constexpr f = [&](auto& a, auto& b)->{return a+b;};",
                     r.variable_capture)
    full_regex_match(
        "constexpr f = [&](auto& a, auto& b)->{\n return a+b; \n};",
        r.variable_capture)

    #function match
    assert r.is_function.match("   int main();")
    assert r.is_function.match("int main() { }")
    assert r.is_function.match("void do_things(const i* const ptr) {}")
    assert r.is_function.match(
        "             virtual std::string get_tag(const std::string& key)=0; ")
    assert not r.is_function.match("auto i =0;")
    assert not r.is_function.match("auto i{0};")
    assert not r.is_function.match("std::vector<std::string> vec{};")
    assert not r.is_function.match(
        r"std::vector<std::string> vec={\"a\",\"b\",\"c\"}; //abc")
    assert not r.is_function.match(
        r"std::vector<std::string> vec=(\"a\",\"b\",\"c\"); //abc")
    assert not r.is_function.match(r"std::vector<std::string> vec=(\n); //abc")
    assert not r.is_function.match("std::vector<std::string> vec\n{\n}\n;")

    full_regex_match("int main();", r.function_capture)
    full_regex_match("int main(){}", r.function_capture)
    full_regex_match("long long get_key(){\n return 42; \n}",
                     r.function_capture)
    full_regex_match("long long get_key(int k){\n return k+42; \n}",
                     r.function_capture)
    full_regex_match("long long \n get_key() \n {\n return 42; \n}",
                     r.function_capture)

    #function parameters extraction
    assert r.function_parameters.search(
        "int main(const std::string& a, const std::vector<int>& vec);")

    assert r.function_parameters.search("int main();")
    assert r.function_parameters.search(
        "int main(const std::string& a, const std::vector<int>& vec = { 1, 2, 3, 4} );"
    )

    #verification that the full parameter list is extracted in all cases
    full_regex_search(
        "int main(const std::string& a, const std::vector<int>& vec);",
        r.function_parameters,
        "(const std::string& a, const std::vector<int>& vec)")

    full_regex_search(
        "int main(const std::string& a, const std::vector<int>& vec = {1,2,3,4});",
        r.function_parameters,
        "(const std::string& a, const std::vector<int>& vec = {1,2,3,4})")

    full_regex_search(
        "int main(const std::string& a, \n const std::vector<int>& vec \n = {1,2,3,4});",
        r.function_parameters,
        "(const std::string& a, \n const std::vector<int>& vec \n = {1,2,3,4})")
