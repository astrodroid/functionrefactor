import re
from functionrefactor.header import *
from functionrefactor.header_components import *
from functionrefactor.string_utilities import *


class Regex():
    ''' contains all the regular expressions used by the parser and some methods that operate on them.
        In most cases however the parsers access the regular expressions as needed'''

    def __init__(self):
        self.preprocessor_c = re.compile(r'#define')
        self.includes = re.compile(r'#include')
        self.generic_preprocessor = re.compile(r'#')
        self.line_continuation = re.compile(r'.*(\\\s*)$')

        self.namespace = re.compile(r'\s*namespace(.*?)\s*\{', flags=re.DOTALL)
        self.class_ = re.compile(r'\s*class(.*?)\s*\{', flags=re.DOTALL)
        self.struct_ = re.compile(r'\s*struct(.*?)\s*\{', flags=re.DOTALL)
        self.union_ = re.compile(r'\s*union(.*?)\s*\{', flags=re.DOTALL)

        self.comment_single_line = re.compile(r'\s*//.*')
        self.comment_multiline = re.compile(r'\s*/\*.*\*/', flags=re.DOTALL)
        self.comment_multiline_begin = re.compile(r'\s*/\*.*', flags=re.DOTALL)
        self.comment_multiline_end = re.compile(r'.*\*/', flags=re.DOTALL)

        self.template = re.compile(r'\s*template')  # look for template start
        # extracts the template arguments
        self.template_args = re.compile(r'\s*<(.*,?)*>', flags=re.DOTALL)

        self.string_block = re.compile(r'\"(.*?)\"')
        self.char_block = re.compile(r'\'(.*?)\'')

        # preceding characters before a c++ variable assignment [a-zA-Z0-9_\-\>\<\: \n]
        # 1st key character is either = or { [=|{] with \ is: ([\=|\{])
        # 2rd key character is either } { or (
        # 3rd key ch. is either } )
        # between any of the key character anything goes
        # its job is to detect if there is a variable defined in the header file.
        # In the source file this might not work if inside a function.
        # c++ comments and strings must be cleaned before this is run

        self.is_variable = re.compile(
            r'[a-zA-Z0-9_\-\>\<\: \n]+([\=|\{]|\;)((.*?)[\(|\}|\{](.*?)[\)|\}]{0,1}){0,1}',
            flags=re.DOTALL)

        self.variable_capture = re.compile(
            r'[a-zA-Z0-9_\-\>\<\: \n]+(.*);', flags=re.DOTALL)
        self.is_function = re.compile(
            r"[a-zA-Z0-9_\-\>\<\: \n]+\((.*?)\)([ \=0]*)", flags=re.DOTALL)
        self.function_capture = re.compile(
            r'[a-zA-Z0-9_\-\>\<\: \n]+(.+?)[\}|\;]$', flags=re.S)
        self.function_parameters = re.compile(r'\((.*?)\)', flags=re.DOTALL)

    def remove_quoted_text(self, text):
        ''' returns text with all instances of quoted text in single and double quotes removed. '''
        return find_and_replace(text, '', self.string_block, self.char_block)

    def remove_comments(self, string):
        '''
        clears any C++ comments // or /* */
        '''

        return find_and_replace(
            string, '', self.comment_single_line, self.comment_multiline,
            self.comment_multiline_begin, self.comment_multiline_end)

    def count_parens_braces(self, text):
        ''' counts how many matches of these are available {,(, [ minus },),]'''

        return len(re.findall(r'[\(|\{|\[]', text)) - len(
            re.findall(r'[\)|\}|\]]', text))

    def iterate_until_match(self,
                            iterator,
                            txt,
                            predicate,
                            balance_operators=True):
        ''' runs through the iterator and outputs the selection (txt),
            untill the predicate lambda returns true, if balance_operators is active it balances
            the parenthesis, braces and square brakets ( { and [] } ) to ensure a full block has been captured.
            It should be ensured that a match will always be found when calling this function.
            Failing that an EOFError will be triggered and this run will be totally borked anyway.
            '''

        while True:
            if not balance_operators and predicate(txt):
                break
            elif balance_operators and predicate(
                    txt) and self.count_parens_braces(
                        self.remove_comments(self.remove_quoted_text(
                            txt))) == 0:
                break
            pos = next(iterator)
            txt = append(txt, pos[1])
        return txt


class Parser():
    ''' Parser'''

    def __init__(self):
        self.rg = Regex()
        self.fun_var_parser = FunctionVariableParser(self.rg)
        self.template_parser = TemplateParser(self.rg)
        self.comment_parser = CommentParser(self.rg)

    def parse_block(self, iterator, first_line, node):
        ''' iterator, first_line is the first_line in this parse call
            (since recursion is used, it might not be the first line)
            Node is an object defined in header.py that implements the Abstract base class interface
        '''
     
        # check for empty space
        if is_invalid(first_line):
            return self.parse_block(iterator, next(iterator)[1], node)

        first_keyword = first_word(self.rg.remove_comments(first_line))

        # the current node has reached its end
        if first_keyword in ["}", "};", "#endif"]:
            return None

        if self.rg.generic_preprocessor.match(first_line):
            self._parse_preprocessor_stuff(iterator, first_line, node)
            return self.parse_block(iterator, next(iterator)[1], node)

        if self.comment_parser.is_match(first_line):
            remainder = self.comment_parser.parse(iterator, first_line, node)
            return self.parse_block(iterator, remainder, node)

        if first_keyword == 'template':
            remainder = self.template_parser.parse(iterator, first_line, node)
            return self.parse_block(iterator, remainder, node)

        if first_keyword == 'namespace':
            remainder = self._parse_namespace_block(iterator, first_line, node)
            return self.parse_block(iterator, remainder, node)

        if first_keyword in ['class', 'struct', 'union']:
            remainder = self._parse_class_block(iterator, first_line, node)
            return self.parse_block(iterator, remainder, node)
        if first_keyword in ['public:', 'private:', 'protected']:
            node.add_component(
                PreprocessorStuff(first_keyword))  # this is treated like text
            return self.parse_block(iterator, '', node)

        remainder = self.fun_var_parser.parse(iterator, first_line, node)
        return self.parse_block(iterator, remainder, node)

    def _parse_preprocessor_stuff(self, iterator, line, node):

        #first looks up for any statement that might be multiline,
        # as long as it is feasible to understand when it ends
        # (macro defines are going to be treated like text instead )
        if first_word(line) in ['#ifdef', '#ifndef', '#if']:
            new_node = node.add_component(PreprocessorStuff(line))

            self.parse_block(iterator, next(iterator)[1], new_node)
            return ""

        if self.rg.line_continuation.search(line):
            node.add_component(PreprocessorStuff(line))
            return ""

        node.add_component(PreprocessorStuff(line))
        return ""

    def _parse_namespace_block(self, iterator, txt, node):

        txt = self.rg.iterate_until_match(
            iterator, txt, lambda t: self.rg.namespace.search(t), False)

        namespace_match = self.rg.namespace.search(txt)
        remainder = find_and_replace_once(txt, '', namespace_match.group(),
                                          '{')
        txt = namespace_match.group()
        if namespace_match:
            # remove the opening braces with space to prevent the name to include an additional '{'
            txt = txt.replace('{', ' ')

            name = nth_word(txt, 2)
            new_node = node.add_component(NamespaceDef(name))

            # catches comments in the same line as the namespace declaration
            self.parse_block(iterator, remainder, new_node)
            return ""

    def _parse_class_block(self, iterator, txt, node):
        txt = self.rg.iterate_until_match(
            iterator, txt,
            lambda t: self.rg.class_.search(t) or self.rg.struct_.search(t) or self.rg.union_.search(t),
            False)

        match = self.rg.class_.search(txt) or self.rg.struct_.search(
            txt) or self.rg.union_.search(txt)
        remainder = find_and_replace_once(txt, '', match.group(), '{')
        txt = match.group()
        if match:
            # remove the opening braces with space to prevent the name to include an additional '{'
            txt = txt.replace('{', ' ')
            _type = first_word(txt)

            name = nth_word(txt, 2)
            new_node = node.add_component(ClassDef(_type, name))

            # catches comments in the same line as the class declaration
            self.parse_block(iterator, remainder, new_node)
            return ""


class TemplateParser():
    def __init__(self, rg):
        self.rg = rg

    def is_match(self, txt):
        return self.rg.template.match(txt)

    def parse(self, iterator, txt, node):

        # look for the full set of template arguments in case they span multiple lines
        txt = self.rg.iterate_until_match(
            iterator, txt, lambda t: self.rg.template_args.search(t), False)
        match = self.rg.template_args.search(txt)
        remainder = find_and_replace_once(txt, '', match.group(), 'template')

        template_args_node = node.add_component(TemplateArgs())
        # replace the equal sign  *if* present with space so that
        # it can be found using the default split function
        txt = txt.replace("=", ' ')
        template_args_list = self.rg.template_args.search(txt).group().split(
            ',')

        self._add_template_args(template_args_list, template_args_node)
        return remainder

    def _add_template_args(self, template_args_list, node):
        # assumes the template arguments are on a separate line
        # from the class/function definition

        for s in template_args_list:
            # remove any *possible* comments in between the arguments
            s = find_and_replace_once(s, '', '<', '>', ',')

            _type = first_word(s)
            _name = nth_word(s, 2)  # 2nd position
            _value = find_and_replace_once(s, '', _type, _name).strip()
            if _type != None and _name != None:
                node.add_component(
                    TemplateArg(_type.strip(), _name.strip(), _value))


class FunctionVariableParser():
    ''' this class does not have is_match() function as that is (almost) certain not to happen.
    This class is used only called after all other options have been disregarded
    '''

    def __init__(self, rg):
        self.rg = rg

    def parse(self, iterator, txt, node):
        [txt, var_match, fun_match] = self._is_variable_or_function(iterator,
                                                                    txt)

        if var_match:
            self._parse_variable(iterator, txt, node)
            return ""
        elif fun_match:
            self._parse_function(iterator, txt, node)
            return ""
        else:
            raise IOError()
            return txt

    def _is_variable_or_function(self, iterator, txt):

        txt = self.rg.iterate_until_match(iterator, txt,
                                          lambda t: self.rg.is_function.match(self.rg.remove_comments(self.rg.remove_quoted_text(t)))
                                          or self.rg.is_variable.match(self.rg.remove_comments(self.rg.remove_quoted_text(t))))

        return [
            txt, self.rg.is_variable.match(txt), self.rg.is_function.match(txt)
        ]

    def _parse_variable(self, iterator, txt, node):
        txt = self.rg.iterate_until_match(
            iterator, txt, lambda t: self.rg.variable_capture.match(t))

        [pre_keywords, name, rhs] = self._extract_variable_components(txt)

        result = node.add_component(Variable(pre_keywords, name, False, rhs))

    def _parse_function(self, iterator, txt, node):

        txt = self.rg.iterate_until_match(
            iterator, txt, lambda t: self.rg.function_capture.match(self.rg.remove_comments(self.rg.remove_quoted_text(t))))

        [keywords, name, func_params, post_keywords,
         body] = self._extract_function_components(txt)
        node.add_component(
            FunctionDef(keywords, name, func_params, post_keywords, body))

    def _extract_variable_components(self, txt):

        [keywords_name, rhs] = fancy_split(txt, ['=', '(', '{', ';'])
        keywords_name_list = keywords_name.split()
        keywords = keywords_name_list[:-1]
        name = keywords_name_list[-1]

        return [[Keywords(k) for k in keywords], name, rhs]

    def _extract_function_components(self, txt):

        function_arguments = self.rg.function_parameters.search(txt).group()

        #the function arguments are extracted via regex separetely
        if function_arguments:
            function_arguments = function_arguments[1:-1]
            txt = find_and_replace_once(txt, '', function_arguments)

        [keywords_name, _ignored, post_keywords, remainder] = fancy_split(
            txt, ['('], [')'], ['{', ':', ';'])
        keywords_name_list = keywords_name.split()

        keywords = keywords_name_list[:-1]
        name = keywords_name_list[-1]

        #by default fancy_split includes the delimitter in the begining,
        #in this case this is not wanted behaviour
        remainder = remainder[1:]
        post_keywords_list = post_keywords[1:].split()

        return [[Keywords(k) for k in keywords], name,
                self._create_function_parameters(function_arguments),
                [Keywords(k) for k in post_keywords_list], ''.join(remainder)]

    def _create_function_parameters(self, args):
        return_val = []
        if is_invalid(args):
            return return_val
        for s in args.split(','):
            [keywords, name, rhs] = self._extract_variable_components(s)
            return_val.append(Variable(keywords, name, True, rhs))

        return return_val


class CommentParser():
    def __init__(self, rg):
        self.rg = rg

    def comment_search(self, txt):
        return self.rg.comment_multiline.search(
            txt) or self.rg.comment_single_line.search(
                txt) or self.rg.comment_multiline_begin.search(
                    txt) or self.rg.comment_multiline_end.search(txt)

    def is_match(self, txt):
        return self.rg.comment_multiline.match(
            txt) or self.rg.comment_single_line.match(
                txt) or self.rg.comment_multiline_begin.match(
                    txt) or self.rg.comment_multiline_end.match(txt)

    def parse(self, iterator, comment, node):
        ''' returns the remaining unprocessed text'''

        single_match = self.rg.comment_single_line.search(comment)
        if single_match:
            node.add_component(Comments(single_match.group()))
            return find_and_replace_once(comment, '', single_match.group())

        multi_match = self.rg.comment_multiline.search(comment)

        if multi_match:
            node.add_component(Comments(multi_match.group()))
            return find_and_replace_once(comment, '', multi_match.group())
        else:
            comment = self.rg.iterate_until_match(
                iterator, comment,
                lambda t: self.rg.comment_multiline.search(t), False)

            multi_match = self.rg.comment_multiline.search(comment)
            # add multiline comment only when the
            if multi_match:
                node.add_component(Comments(multi_match.group()))
                return find_and_replace_once(comment, '', multi_match.group())
