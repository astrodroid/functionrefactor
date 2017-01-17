import subprocess
import sys

__all__ = ['Formatter']


class Formatter():
    ''' Launches clang-format to ensure the input and output is decently formatted'''

    def __init__(self, style_override='Chromium'):
        self.style_override = style_override

    def _open(self, file_path):
        with open(file_path) as f:
            while True:
                line = f.readline()
                if not line:
                    break
                yield line

    def launch_batch(self, lines_list):
        return self.launch(''.join([s + '\n' for s in lines_list]))

    def launch(self, lines):
        command = ['clang-format']
        if self.style_override:
            command = ['clang-format', '-style=' + self.style_override]

        p = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            shell=False)

        _out = p.communicate(input=lines.encode())[0]

        return (_out.decode().split('\n'))

    def open_and_launch(self, file_path):
        ''' launches the clang_format with specified clang_format style if provided.
        It outputs a list of strings properly formatted'''
        lines = ""
        for l in self._open(file_path):
            lines += l

        return self.launch(lines)

     
