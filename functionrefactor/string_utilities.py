import re


def first_word(string):

    for s in string.split():
        if len(s) > 0 or not s.isspace():
            return s

    return ""


def nth_word(string, n):
    counter = 0
    for s in string.split():
        if len(s) > 0 or not s.isspace():
            counter += 1
            if counter == n:
                return s

    return None


def trim_whitespace(string):
    return string.replace(' ', '')


def find_and_replace(string, replace_with_this, *re_args):
    '''
    Finds all matches of the regex array in the string with the replace_with_this string
    '''
    for regex in re_args:
        match = regex.findall(string)

        for m in match:
            string = string.replace(m, replace_with_this, 1)

    return string


def find_and_replace_all(string, replace_with_this,
                         *remove_as_many_times_as_possible):
    ''' finds all the instances of *remove_as_many_times_as_possible strings (it supports many parameters)
        in the input string and replaces them  with replace_with_this'''

    for s in remove_as_many_times_as_possible:
        string = string.replace(s, replace_with_this)

    return string


def find_and_replace_once(string, replace_with_this, *remove_once):
    ''' finds the 1st instance of *remove_once strings (it supports many parameters)
        in the input string and replaces them with replace_with_this'''

    for s in remove_once:
        string = string.replace(s, replace_with_this, 1)

    return string


def find_and_replace_set(string, *replace_tuples):
    ''' finds and replaces all instances of each replace_tuples,
        first is the lookup string and 2nd is the replacement '''
    for t in replace_tuples:
        string = string.replace(t[0], t[1])

    return string


def is_invalid(line):
    return line.isspace() or len(line) < 1


def append(*str):
    '''
    #$ joins a set of strings together, returns the concatenated string and ignores null strings
    '''

    return ''.join([x for x in str if x != None])


def append_list(str, list, separator=''):
    '''
    #$ joins a set of strings together, returns the concatenated string and ignores null strings
    '''

    return_val = ''.join([x + separator for x in list if x != None])
    sep_size = len(separator)
    if len(return_val) > sep_size and sep_size != 0:
        return str + return_val[:-sep_size]
    else:
        return str + return_val


def fancy_split(input_string, *delimeters):
    '''
    Splits the input string *once* based on the delimiters arguments supplied
        example: fancy_split ('aaaa;bbbbb' ,[';'] ) returns ['aaaa',';bbbbb']
    '''
    return_val = []
    i_last = 0

    str_break = enumerate(delimeters)
    delimiter = next(str_break)
    for i, s in enumerate(input_string):
        if s in delimiter[1]:
            return_val.append(input_string[i_last:i])
            i_last = i
            try:
                delimiter = next(str_break)
            except StopIteration:
                return_val.append(input_string[i_last:])
                break
    if len(return_val) == len(delimeters) + 1:
        return return_val
    elif len(return_val) == 0 and len(delimeters) == 1:
        return [input_string, '']
    else:
        print(return_val)
        raise SyntaxError('character missing, split did not fully complete')
        return ['#formaterror'] * (len(delimeters) + 1)
