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
    print("parse_to_file: processing %s, output header: %s, output source: %s"
          % (filename, hpp_file, cpp_file))
    [output_hpp, output_cpp] = parse_header(filename)

    if hpp_file:
        #hpp_file = _get_full_path('', filename, hpp_file, '.hpp')

        with open(hpp_file, 'w') as hpp:
            hpp.writelines(s + '\n' for s in output_hpp)
            print("header file: %s write done" % (hpp_file))
    if cpp_file:
        #cpp_file = _get_full_path('', filename, cpp_file, '.cpp')
        with open(cpp_file, 'w') as cpp:
            cpp.writelines(s + '\n' for s in output_cpp)
            print("source file: %s write done" % (cpp_file))

    if not hpp_file or not cpp_file:
        return [output_hpp, output_cpp]


def launch_cases(jfile_path):
    ''' runs a sets of cases defined in a json file. It need to include a json key "launcher"
    '''
    print("launching cases")
    try:
        with open(jfile_path, "r") as launcher:
            launcher_file = json.load(launcher)
            print("laucher file: %s opened" % jfile_path)
    except FileNotFoundError:
        print('File not found, file_path: ' + file_path)
        return

    settings.update_global_settings(launcher_file)
    launch_list = launcher_file['launcher']
    base_folder = os.path.dirname(launcher.name)
    if base_folder and len(base_folder) > 0:
        base_folder = base_folder + sep

    assert len(launch_list) != 0

    for input_key in launch_list:
        launch_case(base_folder, input_key)


def launch_case(base_folder, jobj_case, launch_list=None):
    if jobj_case['active']:

        sep = os.path.sep
        settings.update_case_settings(jobj_case)

        if jobj_case['overwrite']:
            return parse_to_file(
                base_folder + jobj_case['input'],
                _get_full_path(base_folder, jobj_case['input'],
                               jobj_case['hpp_out'], '.hpp'),
                _get_full_path(base_folder, jobj_case['input'],
                               jobj_case['cpp_out'], '.cpp'))

        else:
            return parse_to_file(base_folder + sep + jobj_case['input'])


def _get_full_path(base_folder, input_file, destination, extension):
    ''' returns the full path for the output file
        based on the input folder and output directory,
         taking into account that the output might be an output path or a filename'''
    print('base_folder: %s, input_file: %s, destination: %s, extension: %s' %
          (base_folder, input_file, destination, extension))

    sep = os.path.sep

    #the input file may contain folders
    input_file_dirname = os.path.dirname(input_file)
    base_folder = base_folder + input_file_dirname
    input_file = os.path.basename(input_file)

    # looking for full path or relative path
    if '.cpp' in destination or '.hpp' in destination:
        return base_folder + destination + extension
    else:
        return base_folder + destination + sep + input_file.replace(".hpp",
                                                              '') + extension


def execute(argv=None):
    if argv is None:
        argv = sys.argv
    main(argv)


def main(args):
    """Entry point for the application script"""
    print(args)
    if len(args) <= 1:
        raise AssertionError
    elif '.json' in args[1]:
        launch_cases(args[1])
    else:
        if len(args) == 2:
            parse_to_file(args[1])
        if len(args) == 3:
            parse_to_file(args[1], args[2])
        if len(args) > 3:
            parse_to_file(args[1], args[2], args[3])


if __name__ == '__main__':
    main(sys.argv)
