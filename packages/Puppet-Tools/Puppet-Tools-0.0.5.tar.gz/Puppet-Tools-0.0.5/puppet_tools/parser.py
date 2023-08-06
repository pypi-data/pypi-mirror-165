import string

from .constants import LOG_TYPE_FATAL, CheckRegex, check_regex_list, LOG_TYPE_ERROR, LOG_TYPE_DEBUG, LOG_MESSAGES
from .puppet_objects.puppet_block import PuppetBlock
from .puppet_objects.puppet_case import PuppetCase
from .puppet_objects.puppet_case_item import PuppetCaseItem
from .puppet_objects.puppet_class import PuppetClass
from .puppet_objects.puppet_include import PuppetInclude
from .puppet_objects.puppet_resource import PuppetResource
from .puppet_objects.puppet_variable import PuppetVariable
from .utility import strip_comments, brace_count_verify, add_log, get_until, get_matching_end_brace, count_newlines, \
    check_regex, ParseHelper


def walk_content(content, puppet_file, line_number=1):
    content = strip_comments(content)
    result = brace_count_verify(content)
    if result == 0:
        block = walk_block(content, line_number, puppet_file)
        puppet_file.add_item(block)
    elif result < 0:
        add_log(puppet_file.name, LOG_TYPE_FATAL, (0, 0), "Too few start braces '{', file can't be parsed", "")
    elif result > 0:
        add_log(puppet_file.name, LOG_TYPE_FATAL, (0, 0), "Too few end braces '}', file can't be parsed", "")

    return puppet_file


def walk_block(content, line_number, puppet_file):
    puppet_block = PuppetBlock()
    index = 0

    while index < len(content):
        char = content[index]

        if char == '\n':
            line_number += 1
            index += 1
        elif char in ['}', '{']:
            index += 1
        elif char == '$':
            helper = ParseHelper(content, index)
            helper.p1().until('=', save=True).p1().until('\n', save=True)

            name, value = helper.results()
            puppet_variable = PuppetVariable(name.lstrip().rstrip())
            puppet_variable.set_value(value.lstrip().rstrip())
            puppet_block.add_item(puppet_variable)
            index = helper.index()
        elif content[index:index + 2] == "->":
            if isinstance(puppet_block.items[-1], PuppetResource):
                puppet_block.items[-1].set_is_dependency()
            else:
                add_log(puppet_file.name, LOG_TYPE_ERROR, (line_number, 0), "Dependency definition invalid",
                        content[index:index + 2])
            index += 3
        elif content[index:index + 7] == "include":
            if not check_regex(content[index:], (line_number, 0), puppet_file, CheckRegex.CHECK_INCLUDE_LINE):
                break

            helper = ParseHelper(content, index)
            helper.ps(8).until([' ', '}'], save=True)
            name = helper.results()[0]
            include = PuppetInclude(name)
            puppet_block.add_item(include)
            index = helper.index()
        elif content[index:index + 4] == "case":
            if not check_regex(content[index:], (line_number, 0), puppet_file, CheckRegex.CHECK_CASE_LINE):
                break
            helper = ParseHelper(content, index)
            c, line_count = helper.ps(5).until('{', save=True).get_content_till_end_brace()
            name = helper.results()[0]
            puppet_case = walk_case(c, name.rstrip(), line_number, puppet_file)
            puppet_block.add_item(puppet_case)
            index = helper.index()
            line_number += line_count
        elif content[index:index + 5] == "class":
            helper = ParseHelper(content, index)
            if check_regex(content[index:], (line_number, 0), puppet_file, CheckRegex.CHECK_CLASS_LINE, disable_log=True):
                c, line_count = helper.ps(6).until('{', save=True).get_content_till_end_brace()
                name = helper.results()[0]
                puppet_class = walk_class(c, name.rstrip(), line_number, puppet_file)
                puppet_block.add_item(puppet_class)
                index = helper.index()
                line_number += line_count
            elif check_regex(content[index:], (line_number, 0), puppet_file, CheckRegex.CHECK_CLASS_LINE2, disable_log=True):
                helper.ps(6).until('{').save_index("brace_index").p1().until(':', save=True)
                c, line_count = helper.get_content_till_end_brace("brace_index")
                name = helper.results()[0]
                puppet_class = walk_class(c, name.rstrip(), line_number, puppet_file)
                puppet_block.add_item(puppet_class)
                index = helper.index()
                line_number += line_count
            else:
                log_type, message = LOG_MESSAGES[CheckRegex.CHECK_CLASS_LINE]
                add_log(puppet_file.name, log_type, (line_number, 0), message, content[index:])
                break

        else:
            items = [len(i) for i in PuppetResource.TYPES
                     if content[index:].startswith(i) and "=>" not in get_until(content[index:], "\n", or_char=":")[0]]

            if len(items) == 1:
                text, size = get_until(content[index:], "\n")
                if not check_regex(text, (line_number, 0), puppet_file, CheckRegex.CHECK_RESOURCE_FIRST_LINE):
                    _, size = get_until(content[index:], '}')
                    index += size
                else:
                    item_len = items[0]
                    name = content[index:index + item_len]
                    index += item_len

                    helper = ParseHelper(content, index)
                    c, line_count = helper.until('{').get_content_till_end_brace()
                    puppet_resource = walk_resource(c, name, line_number, puppet_file)
                    puppet_block.add_item(puppet_resource)
                    index = helper.p1().index()
                    line_number += line_count
            else:
                if content[index] != ' ':
                    text, size = get_until(content[index:] + '\n', "\n")
                    add_log(puppet_file.name, LOG_TYPE_DEBUG, (line_number, 0), "Unimplemented? while walking block",
                            text)
                    index += size
                index += 1
    return puppet_block


def walk_class(content, name, line_number, puppet_file):
    puppet_class = PuppetClass(name)
    puppet_block = walk_block(content, line_number, puppet_file)
    puppet_class.add_item(puppet_block)
    return puppet_class


def walk_case(content, name, line_number, puppet_file):
    puppet_case = PuppetCase(name)
    index = 0

    while index < len(content):
        char = content[index]
        if char == "'" or char == "\"":
            if not check_regex(content[index:], (line_number, 0), puppet_file, CheckRegex.CHECK_CASE_ITEM_LINE):
                break
            helper = ParseHelper(content, index)
            c, line_count = helper.p1().until(["'", '"'], save=True).until(':').until('{').get_content_till_end_brace()
            name = helper.results()[0]
            puppet_case_item = PuppetCaseItem(name)
            puppet_block = walk_block(c, line_number, puppet_file)
            puppet_case_item.add_item(puppet_block)
            puppet_case.add_item(puppet_case_item)
            index = helper.p1().index()
            line_number = line_count
        elif char == '\n':
            line_number += 1
            index += 1
        else:
            index += 1

    return puppet_case


def walk_resource(content, typ, line_number, puppet_file):
    puppet_resource = PuppetResource(typ, line_number, puppet_file.name)
    helper = ParseHelper(content, 0)
    helper.until(["'", '"']).p1().until(["'", '"'], save=True).until(':').p1()
    index = helper.index()
    puppet_resource.name = helper.results()[0]

    while index < len(content):
        char = content[index]

        if char == '\n':
            # Found end of line
            line_number += 1
            index += 1
        elif char == '}':
            index += 1
        elif char != ' ':
            text, size = get_until(content[index:], ";", or_char='\n')
            text2, _ = get_until(content[index + size + 1:] + "\n", "\n")
            if check_regex(text, (line_number, 0), puppet_file, CheckRegex.CHECK_RESOURCE_ITEM_POINTER):
                if check_regex(text, (line_number, 0), puppet_file, CheckRegex.CHECK_RESOURCE_ITEM_VALUE):
                    # Next one may be ignored but makes a difference for the next check
                    if not check_regex_list[CheckRegex.CHECK_RESOURCE_ITEM_COMMA_NEXT_LINE_END].match(text + text2):
                        check_regex(text, (line_number, 0), puppet_file, CheckRegex.CHECK_RESOURCE_ITEM_COMMA)
                        puppet_resource.add_item(text)
                    else:
                        check_regex(text, (line_number, 0), puppet_file, CheckRegex.CHECK_RESOURCE_ITEM_COMMA_WARN)
                        puppet_resource.add_item(text)
            index += size if size > 0 else 1
        else:
            index += 1
    return puppet_resource
