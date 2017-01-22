from functionrefactor.header import HeaderDef
from functionrefactor.parser import Parser
from functionrefactor.formatter import Formatter
from functionrefactor.settings import *
import sys
import os
import json

__all__ = ['parse_header', 'parse_to_file', 'main']


#
def parse_header(filename):
    parser = Parser()
    clang_formatter = Formatter()

    path_name = os.path.splitext(os.path.basename(filename))[0]

    text = clang_formatter.open_and_launch(filename)
    it = enumerate(text)

    header_root = HeaderDef()
    try:
        parser.parse_block(it, next(it)[1], header_root)
    except StopIteration:
        pass
    return [
        clang_formatter.launch_batch(header_root.get_lines_hpp()),
        clang_formatter.launch_batch(
            header_root.get_lines_cpp(path_name + ".hpp"))
    ]


def parse_to_file(filename, hpp_file=None, cpp_file=None):
    ''' filename: the input header to be processed
        hpp_file: the output header
        cpp_file the output cpp file
        If any of the output hpp/cpp files is emited the parse header will be returned.
        This is intended for use in testing'''
    [output_hpp, output_cpp] = parse_header(filename)

    if hpp_file:
        with open(hpp_file, 'w') as hpp:
            hpp.writelines(s + '\n' for s in output_hpp)
    if cpp_file:
        with open(cpp_file, 'w') as cpp:
            cpp.writelines(s + '\n' for s in output_cpp)

    if not hpp_file or not cpp_file:
        return [output_hpp, output_cpp]


def launch_cases(jfile_path):
    ''' runs a sets of cases defined in a json file. It need to include a json key "launcher"
    '''
    try:
        with open(jfile_path, "r") as launcher:
            launcher_file = json.load(launcher)
    except FileNotFoundError:
        print('File not found, file_path: ' + file_path)
        return

    settings.update_global_settings(launcher_file)
    launch_list = launcher_file['launcher']
    base_folder = os.path.dirname(launcher.name)

    for input_key in launch_list:
        launch_case(base_folder, input_key)


def launch_case(base_folder, jobj_case, launch_list=None):
    if jobj_case['active']:

        sep = os.path.sep
        settings.update_case_settings(jobj_case)

        file_name = os.path.splitext(os.path.basename(jobj_case['input']))[0]
        if jobj_case['overwrite']:
            return parse_to_file(
                path + sep + jobj_case['input'],
                path + sep + jobj_case['hpp_out'] + file_name + '.hpp',
                path + sep + jobj_case['cpp_out'] + file_name + '.cpp')
        else:
            return parse_to_file(path + sep + jobj_case['input'])


def execute(argv=None):
    if argv is None:
        argv = sys.argv
    main(argv)


def main(args):
    """Entry point for the application script"""
    if len(args) == 0:
        launch_cases('.functionrefactor.json')
    elif '.json' in args[0]:
        launch_cases(args[0])
    else:
        if len(args) == 2:
            parse_to_file(args[1])
        if len(args) == 3:
            parse_to_file(args[1], args[2])
        if len(args) > 3:
            parse_to_file(args[1], args[2], args[3])


if __name__ == '__main__':
    main(sys.argv)
