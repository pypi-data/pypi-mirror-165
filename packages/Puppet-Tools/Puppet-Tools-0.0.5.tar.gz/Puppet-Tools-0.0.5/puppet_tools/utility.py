import os
import re

from .constants import LOG_MESSAGES, CheckRegex, check_regex_list, LOG_TYPE_ERROR

log_list = []


class ParseHelper:
    def __init__(self, content, index):
        self.content = content
        self.ind = index
        self.results_list = []
        self.index_save = {}

    def p1(self):
        self.ind += 1
        return self

    def ps(self, size):
        self.ind += size
        return self

    def until(self, chars, save=False):
        if type(chars) == str:
            chars = [chars]
        res, size = get_until(self.content[self.ind:], chars)
        self.ind += size
        if save:
            self.results_list.append(res)
        return self

    def get_content_till_end_brace(self, override_index=None):
        ind = get_matching_end_brace(self.content, self.index_save[override_index] if override_index else self.ind)
        c = self.content[self.ind:ind]
        self.ind += ind - self.ind
        return c, count_newlines(c)

    def save_index(self, name: str):
        self.index_save[name] = self.ind
        return self

    def results(self):
        return self.results_list

    def index(self):
        return self.ind


def strip_comments(code):
    code = str(code)
    return re.sub(r'(?m)^ *#.*\n?', '\n', code)


def add_log(file_name, typ, line_col, message, string):
    global log_list
    log_list.append((file_name, typ, line_col, message, string))


def logs_contains_error():
    return any([i[1] >= LOG_TYPE_ERROR for i in log_list])


def clear_logs():
    global log_list
    log_list = []


def get_logs():
    return log_list


def check_regex(string, line_col, file, regex_check_name: CheckRegex, disable_log=False):
    pattern = check_regex_list[regex_check_name]
    success = bool(pattern.match(string))
    if not success and not disable_log:
        log_type, message = LOG_MESSAGES[regex_check_name]
        add_log(file.name, log_type, line_col, message, string)
    return success


def get_all_files(path, include_dirs=False):
    path = os.path.normpath(path)
    path = os.path.abspath(path)
    print("Path: ", path)
    res = []
    for root, dirs, files in os.walk(path, topdown=True):
        if include_dirs:
            res += [os.path.join(root, d) for d in dirs]
        res += [os.path.join(root, f) for f in files]

    return res


def get_file_contents(path):
    with open(path, 'r') as f:
        return f.read()


def find_next_char(content, chars):
    index = 0

    while content[index] not in chars:
        index += 1

    return index


def find_next_string(content, string):
    index = 0
    while content[index:index + len(string)] != string:
        index += 1
    return index


def get_until(content, chars=None, string=None, or_char=None):
    size = 0
    if type(chars) == str:
        chars = [chars, or_char]
    if chars:
        size = find_next_char(content, chars)
    elif string:
        size = find_next_string(content, string)

    return content[:size], size


def brace_count_verify(content):
    return content.count('{') - content.count('}')


def get_matching_end_brace(content, index):
    if content[index] != '{':
        raise Exception("char is not a {, found: '%s'" % content[index])
    counter = 0
    end_brace_found = False
    try:
        while counter != 0 or not end_brace_found:
            if content[index] == '{':
                counter += 1
            if content[index] == '}':
                counter -= 1
                end_brace_found = True
            index += 1
    except IndexError as e:
        print(counter, end_brace_found)
        raise IndexError(str(e) + ": " + str(counter) + " " + str(end_brace_found))
    return index


def count_newlines(content):
    return len(content.split('\n'))
