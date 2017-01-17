from functionrefactor.string_utilities import *
from functionrefactor.header_components import *

__all__ = ['PreprocessorStuff', 'ClassDef', 'NamespaceDef', 'HeaderDef']


class PreprocessorStuff(Abstract):
    """Preprocessor things like #includes, #ifdef and MACROS"""

    def __init__(self, text):
        self.text = text
        self.nested_declarations = []

    def format_cpp(self, parent, override_andshow):
        key = first_word(self.text).strip()
        #main thing this if statement does is to check for variables that are to be moved in the cpp file
        #OR an override from the parent class
        # the first #ifdef, #if is the parent class and subequent statements are all child of the same parent
        if self.is_visible_in_cpp():
            return self.text + " " + ''.join([
                d.format_cpp(parent, True) + '\n'
                for d in self.nested_declarations
            ]) + "\n#endif"
        elif override_andshow:
            return self.text + " " + ''.join([
                d.format_cpp(parent, True) + '\n'
                for d in self.nested_declarations
            ])
        elif key in [
                '#define', '#include', 'public:', 'private:', 'protected:'
        ]:
            return ''
        else:
            return ''.join([
                d.format_cpp(parent, False) + '\n'
                for d in self.nested_declarations
            ])

    def format_hpp(self, parent):
        key = first_word(self.text).strip()
        if key in ['#if', '#ifndef', '#ifdef']:
            return self.text + '\n' + ''.join([
                d.format_hpp(parent) + '\n' for d in self.nested_declarations
            ]) + "\n#endif"
        else:
            return self.text + '\n' + ''.join([
                d.format_hpp(parent) + '\n' for d in self.nested_declarations
            ])

    def add_component(self, component):
        self.nested_declarations.append(component)
        return self.nested_declarations[-1]

    def get_name(self):
        return None

    def get_type(self):
        return 'PreprocessorStuff'

    def is_visible_in_cpp(self):
        return 'FunctionDef' in [
            d.get_type() for d in self.nested_declarations
            if d.is_visible_in_cpp()
        ]


class ClassDef(Abstract):
    """
    type: class or struct or even union as this script doesn't care what it is
    private_declarations is all variab

    """

    def __init__(self, _type, name):
        self.type = _type
        self.name = name
        self.components = []

    def deactivate_conversion(self):
        self.is_active = False

    def add_component(self, d):
        '''
        expects an already constructed object that implements:
         format_cpp and format_hpp methods
         returns last element
        '''
        print(d.get_type())
        self.components.append(d)
        return d

    def _format_begin(self):
        return self.type + " " + self.name + " {\n"

    def _format_end(self):
        return "}; \n"

    def format_cpp(self, parent, *_):
        show_it = True
        return_val = "\n"

        for i in range(len(self.components)):
            _elem = self.components[i]
            if i < len(self.components) - 1:
                _next = self._get_next(i)
                #ensure comment linked to something visible is also shown

                show_it = _next.is_visible_in_cpp() and _elem.get_type(
                ) == 'Comments' or _elem.is_visible_in_cpp()

            else:
                show_it = _elem.is_visible_in_cpp()
            if show_it:
                return_val = append(return_val, _elem.format_cpp(self, True),'\n')

        return return_val + '\n'

    def format_hpp(self, parent):
        return_val = self._format_begin()

        for d in self.components:
            return_val = append(return_val, d.format_hpp(self))

        return_val = append(return_val, self._format_end(),'\n')
        return return_val

    def get_name(self):
        return self.name

    def get_type(self):
        return 'ClassDef'

    def is_visible_in_cpp(self):
        return 'FunctionDef' in [
            d.get_type() for d in self.components if d.is_visible_in_cpp()
        ]

    def _get_next(self, start_index):
        return next(d for index, d in enumerate(self.components)
                    if index > start_index)


class NamespaceDef(Abstract):
    """ defines a namespace
    name: is the name of the namespace`
    nested_declarations: all declarations that are within the namespace block, other namespaces, classes functions, namespace scope variables etc...
    """

    def __init__(self, name):
        self.name = name
        self.nested_declarations = []

    def add_component(self, declaration):
        self.nested_declarations.append(declaration)
        return declaration

    def is_visible_in_cpp(self, *_):
        return True

    def _format_begin(self):
        return "namespace " + self.name + " {\n"

    def _format_end(self):
        return "}// namespace " + self.name + "\n"

    def format_cpp(self, parent, *_):
        return_val = self._format_begin()
        for d in self.nested_declarations:
            return_val = append(return_val, d.format_cpp(self, False))

        return_val = append(return_val, self._format_end())
        return return_val

    def format_hpp(self, parent):
        return_val = self._format_begin()
        for d in self.nested_declarations:
            return_val = append(return_val, d.format_hpp(self))

        return_val = append(return_val, self._format_end())
        return return_val

    def get_name(self):
        return self.name

    def get_type(self):
        return 'NamespaceDef'


class HeaderDef(Abstract):
    """ contains all the header declarations tree including namespace, functions etc
        the decision of what is to be included in the cpp or hpp file is up to the nested_declarations objects
    """

    def __init__(self):
        self.nested_declarations = []

    def add_component(self, declaration):
        self.nested_declarations.append(declaration)
        return declaration

    def clear(self):
        self.nested_declarations = []

    def is_visible_in_cpp(self, *_):
        return False

    def format_cpp(self, header_name=None):
        return_val = "\n"
        if header_name:
            return_val = "#import  \"" + header_name + "\"\n"
        for d in self.nested_declarations:
            return_val = append(return_val, d.format_cpp(self, False))

        #return_val = append(return_val, "\n")
        return return_val

    def get_lines_cpp(self, header_file=None):
        '''returns the program output (source cpp file) splitted into lines'''
        return self.format_cpp(header_file).split('\n')

    def format_hpp(self):
        return_val = "\n"

        for d in self.nested_declarations:
            return_val = append(return_val, d.format_hpp(self))

        #return_val = append(return_val, "\n")
        #print(" return_val: " + return_val + "nested_declarations size:")
        # print(len(self.nested_declarations))
        return return_val

    def get_lines_hpp(self):
        '''returns the program output (header file) splitted into lines'''
        return self.format_hpp().split('\n')

    def get_name(self):
        return None

    def get_type(self):
        return 'HeaderDef'
