from functionrefactor.parser import Parser
from functionrefactor.header import *
from tests.common_functions import *

# yapf: disable
_in = [
        "#define SMACRO = ()... ; /*  */","#define OLDSTYLECONST = 42",

        r"#define MULTILINE_MACRO = DOSOMETHING()\ ",
            r" return -1;\ ",

        "#ifdef SOMETHING",
            "int do_somethingelse()",
           "            {return v;}",
        "#else ",
            " int dont_do_nothing() {return 0;}",
        "#endif",

        "#ifdef CONSTANT //This explains something about something ",
        "     std::vector<std::string> text{ }",
         "#endif", ''
    ]


expected_result_hpp = [
    "#define SMACRO = ()... ; /*  */",
    "#define OLDSTYLECONST = 42",

     r"#define MULTILINE_MACRO = DOSOMETHING()\ ",
            r" return -1;\ ",""

        "#ifdef SOMETHINGint do_somethingelse();#else int dont_do_nothing();#endif",

     "#ifdef CONSTANT //This explains something about somethingstd::vector<std::string> text{ }#endif"
]

expected_result_cpp = ["","","","","" "#ifdef SOMETHING int do_somethingelse(){return v ; } #else  int dont_do_nothing(){return 0 ; } #endif"

]


# yapf: enable
def test_preproc():
    ''' ignores_new lines '''

    parser = Parser()

    parse_batch_run(
        _in, expected_result_hpp, expected_result_cpp,
        lambda i, pos, h: parser._parse_preprocessor_stuff(i, pos, h))


def test_preproc_parser():
    ''' uses main parse function parse_block which determines what is contained in each line 
    '''
    parser = Parser()
    parse_batch_run(_in, expected_result_hpp, expected_result_cpp,
                    lambda i, pos, h: parser.parse_block(i, pos, h))
