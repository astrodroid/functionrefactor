from functionrefactor.settings import settings
from functionrefactor.string_utilities import append, append_list, is_invalid, first_word
from abc import ABC, abstractmethod
import re

__all__ = [
    'Abstract', 'Comments', 'TemplateArgs', 'TemplateArg', 'Keywords',
    'Variable', 'FunctionDef'
]


class Abstract(ABC):
    """abstract base class ensures and interface consistency """

    def __init__(self):
        super(AbstractOperation, self).__init__()

    @abstractmethod
    def format_cpp(self, parent, override_andshow=False):
        pass

    @abstractmethod
    def format_hpp(self, parent):
        pass

    @abstractmethod
    def add_component(self, component):
        pass

    @abstractmethod
    def get_name(self):
        return None

    @abstractmethod
    def get_type(self):
        return None

    ''' defaults to false:
        Note that if a parent is not visible the children might be visible
        still for example a class declaration and definition is expected in the header
        but the implemntation of the functions is in the source file,
        if the parent class needs to override the default normal behaviour
        then the format_cpp has that option that is only used in the comment class so far
         '''

    def is_visible_in_cpp(self):
        return False


class Comments(Abstract):
    """comment string goes here"""

    def __init__(self, _comments):
        self.comments = _comments.strip()
        self.set_multiline_comment = False

    def __format(self):
        # return a empty string in cases the comments are null to avoid
        # creating too many new lines
        if self.comments.isspace():
            return ""

        if self.set_multiline_comment:
            self.comments.replace("//", "")
            return "/* " + self.comments + " */\n"
        else:
            return self.comments + "\n"

    def format_cpp(self, parent, override_andshow=False):
        if override_andshow:
            return self.__format()
        else:
            return "\n"

    def format_hpp(self, *_):
        return self.__format()

    def add_component(self, component):
        pass

    def get_name(self):
        return None

    def get_type(self):
        return 'Comments'

    def is_visible_in_cpp(self):
        return False


class TemplateArgs(Abstract):
    def __init__(self):
        self.args = []

    def add_component(self, arg):
        self.args.append(arg)

    def _all_arguments_tobeconverted(self):
        for t in self.args:
            if not t.is_active:
                return False
        return True

    def _format_template(self):
        return_val = "template\n<"
        for i, t in enumerate(self.args):
            if (not t.is_active):
                return_val = append(return_val, t._type, " ", t._name)

                if i < len(self.args) - 1:
                    return_val = append(return_val, ", ")

        return_val = append(return_val, ">\n")
        return return_val

    def format_hpp(self, *_):
        return_val = ''.join(
            [t.format_hpp() for t in self.args if t.is_active])

        if not self._all_arguments_tobeconverted():
            return_val = append(self._format_template(), return_val)
        return return_val

    def format_cpp(self, *_):
        return ""

    def get_name(self):
        return None

    def get_type(self):
        return 'TemplateArgs'


class TemplateArg(Abstract):
    """definition of a template argument
    name is the alias of thetype
    type is whatever is a an typename/class or some kind of constant like int (for example)
    templates are replaced by a using statement, and constants (within a template) are replaced with a constexpr constant
    If a default value is given for the template parameter, then that is used
    """

    def __init__(self, _type, _name, default_value=None):

        self.name = _name
        self.type = _type
        self.is_active = True
        if default_value == None or default_value == "":
            self.default_value = "change_this"
        else:
            self.default_value = default_value

    def deactivate_conversion(self):
        '''deactivates the conversion of this template argument,
        will be outouted as template <typename self.name>'''
        self.is_active = False

    def set_argument_replacement(self, replace_with_this):
        """replaces reference to this tempate argument with the following variable,
        if not set it will be replaced with a using statement where the end user
        will need to specify the correct type
        """

        self.replacement = replace_with_this

    def format_hpp(self, *_):
        if not self.is_active:
            return ""

        if self.type == "class" or self.type == "typename":
            return "using " + self.name + " = " + self.default_value + ";\n"
        else:
            return "constexpr " + self.type + " " + self.name + " = " + self.default_value + ";\n"

    def format_cpp(self, *_):
        return ""

    def add_component(self, component):
        pass

    def get_name(self):
        return None

    def get_type(self):
        return 'TemplateArg'


class Keywords(Abstract):
    """definition of keywords included, examples of keywords include const,
    inline, override, virtual, noexcept, a config file determines which of these
    keywords are to be placed in the cpp file as well and which are not"""

    def __init__(self, value):
        self.keyword_value = value

    def format_hpp(self):
        return self.keyword_value + " "

    def format_cpp(self, *_):
        if self.is_visible_in_cpp:
            return self.keyword_value + " "
        else:
            return ""

    def add_component(self, component):
        pass

    def get_name(self):
        return self.keyword_value

    def get_type(self):
        return 'Keywords'

    def is_visible_in_cpp(self):
        return settings.use_keyword_in_cpp(self.keyword_value)


class Variable(Abstract):
    """definition of a single argument type in a class
    key_words: const or anything else that might apply here
    name: this is what you call that variable
    is_function_argument: prevents adding ";" for function arguments variables
    rhs is the rhs of the variable equal excluded
    """

    def __init__(self, key_words, name, is_function_argument, rhs):
        self.name = name
        self.key_words = key_words
        if is_invalid(rhs):
            self.rhs = None
        else:
            self.rhs = rhs

        self.is_function_argument = is_function_argument
        self.is_active = True

    def deactivate_conversion(self):
        self.is_active = False

    def _format(self, parent):
        #classdef type is garanteed to have a name
        if parent != None and parent.get_type() == 'ClassDef':
            return ''.join([x.format_hpp() for x in self.key_words
                            ]) + parent.get_name() + "::" + self.name
        else:
            return ''.join(
                [x.format_hpp() for x in self.key_words]) + self.name

    def format_hpp(self, *_):
        if is_invalid(self.name):
            return ''
        return_val = self._format(None)
        if self.rhs:
            return_val = append(return_val, self.rhs)

        return return_val

    def format_cpp(self, parent, *_):
        #static variables need to initialised in the cpp file
        if self.is_visible_in_cpp(parent):
            return self._format(parent) + self.rhs

        if self.is_function_argument:
            return self._format(None)

        return ""

    def add_component(self, component):
        pass

    def get_name(self):
        return self.name

    def get_type(self):
        return 'Variable'

    def is_visible_in_cpp(self, *_):
        return "static" in [x.format_hpp() for x in self.key_words]


class FunctionDef(Abstract):
    """definition of a function/void
        pre_keywords: is what is on the left of the function name including returning type etc etc etc
        name: is what you call the function
        function_args: all the inputs Variable List
        """

    def __init__(self, pre_keywords, name, function_args, post_keywords,
                 func_body):
        self.pre_keywords = pre_keywords
        self.name = name
        self.function_args = function_args
        self.post_keywords = post_keywords
        self.function_body = func_body
        self.is_active = True
        self.initialiser_list_re = re.compile(r'[\"\'\.\(\)\,a-zA-Z0-9\s]*\{')

    def deactivate_conversion(self):
        self.is_active = False

    def _format_function_declaration(self, parent):
        ''' formats a function excluding it's implementation
                handles the case where the parent is a class type adding the ParentName:: before the function name '''
        # returntype const etc..
        return_val = ''.join([x.format_cpp() for x in self.pre_keywords])

        if parent != None and parent.get_type() == 'ClassDef':
            return_val = append(
                return_val, " " + parent.get_name() + "::" + self.name + "(")
        else:
            return_val = append(return_val, self.name + "(")
        if parent:
            return_val = append_list(
            return_val, [k.format_cpp(parent) for k in self.function_args],
            ', ') + ')'
        else:
                return_val = append_list(
                return_val, [k.format_hpp(parent) for k in self.function_args],
                ', ') + ')'
        # any further keywords such as const noexcept etc...
        return append_list(return_val,
                           [k.format_cpp() for k in self.post_keywords])

    def _format_function_implementation(self, parent):
        if is_invalid(self.function_body):
            return "\n {\n" + "\n}\n"
        elif len(self.pre_keywords) == 0 and self.initialiser_list_re.match(
                self.function_body):  #constructor with an initialiser list
            return ':' + self.function_body
        else:
            return "{\n" + self.function_body

    def format_cpp(self, parent, *_):
        """format_cpp: formats a file to export in a cpp file"""
        if not self.is_visible_in_cpp():
            return ''
        return self._format_function_declaration(
            parent) + self._format_function_implementation(parent)

    def format_hpp(self, *_):
        if not self.is_visible_in_cpp():
            return self._format_function_declaration(
                None) + self._format_function_implementation(None)
        # returntype const etc..
        return self._format_function_declaration(None) + ';'

    def add_component(self, component):
        pass

    def get_name(self):
        return self.name

    def get_type(self):
        return 'FunctionDef'

    def is_visible_in_cpp(self):
        ''' looks for keys which imply the function is not to be moved over, for example inline'''

        for keya in self.pre_keywords:
            if settings.dont_move_oncpp_ifpresent(keya.get_name()):
                return False
        for keyb in self.post_keywords:
            if settings.dont_move_oncpp_ifpresent(keyb.get_name()):
                return False
        return True
