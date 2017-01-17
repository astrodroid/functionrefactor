from functionrefactor.header import HeaderDef
from functionrefactor.parser import Parser
from functionrefactor.formatter import Formatter
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
    [output_hpp, output_cpp] = parse_header(filename)

    if not output_hpp:
        print("HeaderFile: ")
        print(output_hpp)
    else:
        with open(hpp_file, 'w') as hpp:

            hpp.writelines(s + '\n' for s in output_hpp)

    if not output_cpp:
        print("SourceFile: ")
        print(output_cpp)

    else:
        with open(cpp_file, 'w') as cpp:
            cpp.writelines(s + '\n' for s in output_cpp)


def load_launcher(file_path):

    try:
        with open(file_path, "r") as launcher:
            launcher_file = json.load(launcher)
    except FileNotFoundError:
        print('File not found, file_path: ' + file_path)
        return

    launch_list = launcher_file['launcher']
    path = os.path.dirname(launcher.name)
    sep = os.path.sep

    print('path: ' + path)

    for input_file in launch_list:

        if input_file['active']:
            file_name = os.path.splitext(
                os.path.basename(input_file['input']))[0]
            print('input:')
            print(file_name)
            parse_to_file(
                path + sep + input_file['input'],
                path + sep + input_file['hpp_out'] + file_name + '.hpp',
                path + sep + input_file['cpp_out'] + file_name + '.cpp')


def main(*args):
    """Entry point for the application script"""
    if len(args[0]) == 0:
        load_launcher('.functionrefactor.json')
    elif '.json' in args[0][1]:
        load_launcher(args[0][1])
    else:
        parse_to_file(args)


if __name__ == '__main__':
    main(sys.argv)
