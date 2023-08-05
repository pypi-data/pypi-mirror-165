#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import json
import getpass
import traceback
import inspect
from pawnlib.typing import converter, date_utils, list_to_oneline_string
from pawnlib.config import pawnlib_config as pawn, global_verbose


_ATTRIBUTES = dict(
    list(zip([
        'bold',
        'dark',
        '',
        'underline',
        'blink',
        '',
        'reverse',
        'concealed'
    ],
        list(range(1, 9))
    ))
)
del _ATTRIBUTES['']


_HIGHLIGHTS = dict(
    list(zip([
        'on_grey',
        'on_red',
        'on_green',
        'on_yellow',
        'on_blue',
        'on_magenta',
        'on_cyan',
        'on_white'
    ],
        list(range(40, 48))
    ))
)


_COLORS = dict(
    list(zip([
        'grey',
        'red',
        'green',
        'yellow',
        'blue',
        'magenta',
        'cyan',
        'white',
    ],
        list(range(30, 38))
    ))
)


_RESET = '\033[0m'


def colored(text, color=None, on_color=None, attrs=None):
    """Colorize text.

    Available text colors:
        red, green, yellow, blue, magenta, cyan, white.

    Available text highlights:
        on_red, on_green, on_yellow, on_blue, on_magenta, on_cyan, on_white.

    Available _ATTRIBUTES:
        bold, dark, underline, blink, reverse, concealed.

    Example:
        colored('Hello, World!', 'red', 'on_grey', ['blue', 'blink'])
        colored('Hello, World!', 'green')
    """
    if os.getenv('ANSI_COLORS_DISABLED') is None:
        fmt_str = '\033[%dm%s'
        if color is not None:
            text = fmt_str % (_COLORS[color], text)

        if on_color is not None:
            text = fmt_str % (_HIGHLIGHTS[on_color], text)

        if attrs is not None:
            for attr in attrs:
                if attr is not None:
                    text = fmt_str % (_ATTRIBUTES[attr], text)

        text += _RESET
    return text


def cprint(text, color=None, on_color=None, attrs=None, **kwargs):
    """Print colorize text.
    It accepts arguments of print function.

    :param text:
    :param color:
    :param on_color:
    :param attrs:
    :param kwargs:
    :return:

    Example:
        .. code-block:: python

            cprint("message", "red")  # >>  message

    """

    print((colored(text, color, on_color, attrs)), **kwargs)


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    GREEN = '\033[32;40m'
    CYAN = '\033[96m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    ITALIC = '\033[1;3m'
    UNDERLINE = '\033[4m'
    WHITE = '\033[97m'
    DARK_GREY = '\033[38;5;243m'
    LIGHT_GREY = '\033[37m'


class TablePrinter(object):
    "Print a list of dicts as a table"

    def __init__(self, fmt=[], sep='  ', ul="-"):
        """

        :param fmt: list of tuple(heading, key, width)

                    heading: str, column label \n
                    key: dictionary key to value to print \n
                    width: int, column width in chars \n

        :param sep: string, separation between columns
        :param ul: string, character to underline column label, or None for no underlining

        Example:
            .. code-block:: python

                from pawnlib import output

                nested_data = {
                        "a": {
                            "b": "cccc",
                            "sdsd": {
                                "sdsds": {
                                    "sdsdssd": 2323
                                }
                            },
                            "d": {
                                "dd": 1211,
                                "cccc": "232323"
                            }
                        }
                    }
                fmt = [
                    ('address',       'address',          10),
                    ('value',       'value',          15)
                ]
                cprint("Print Table", "white")
                print(output.TablePrinter(fmt=fmt)(data))
                print(output.TablePrinter()(data))

        """
        super(TablePrinter, self).__init__()
        self._params = {"sep": sep, "ul": ul}

        self.fmt = str(sep).join('{lb}{0}:{1}{rb}'.format(key, width, lb='{', rb='}') for heading, key, width in fmt)
        self.head = {key: heading for heading, key, width in fmt}
        self.ul = {key: str(ul) * width for heading, key, width in fmt} if ul else None
        self.width = {key: width for heading, key, width in fmt}
        self.data_column = []

    def row(self, data, head=False):
        if head:
            return self.fmt.format(**{k: get_bcolors(data.get(k), "WHITE", bold=True, width=w) for k, w in self.width.items()})
        else:
            return self.fmt.format(**{k: str(data.get(k, ''))[:w] for k, w in self.width.items()})

    def get_unique_columns(self):
        self.data_column = []
        for item in self.data:
            self.data_column = self.data_column + list(item.keys())

        self.data_column = list(set(self.data_column))
        self.data_column.sort()

    def __call__(self, data_list):
        if len(self.fmt) == 0:
            sep = self._params.get("sep")
            ul = self._params.get("ul")

            self.data = data_list
            self.get_unique_columns()

            # fmt = list(dataList[0].keys())
            fmt = self.data_column

            width = 12
            self.fmt = str(sep).join('{lb}{0}:{1}{rb}'.format(key, width, lb='{', rb='}') for key in fmt)
            self.width = {key: width for key in fmt}
            self.ul = {key: str(ul) * width for key in fmt} if ul else None
            self.head = {key: key for key in fmt}
            # self.head  = {key:get_bcolors(key, "WHITE", bold=True) for key in fmt}

        _r = self.row
        res = [_r(data) for data in data_list]
        res.insert(0, _r(self.head, head=True))
        if self.ul:
            res.insert(1, _r(self.ul))
        return '\n'.join(res)


def get_bcolors(text, color, bold=False, underline=False, width=None):
    """

    Returns the color from the bcolors object.

    :param text:
    :param color:
    :param bold:
    :param underline:
    :param width:
    :return:
    """
    if width and len(text) <= width:
        text = text.center(width, ' ')
    return_text = f"{getattr(bcolors, color)}{text}{bcolors.ENDC}"
    if bold:
        return_text = f"{bcolors.BOLD}{return_text}"
    if underline:
        return_text = f"{bcolors.UNDERLINE}{return_text}"
    return str(return_text)


def colored_input(message, password=False, color="WHITE"):
    input_message = get_bcolors(text=message, color=color, bold=True, underline=True) + " "
    if password:
        return getpass.getpass(input_message)
    return input(input_message)


def get_colorful_object(v):
    if type(v) == bool:
        value = f"{bcolors.ITALIC}"
        if v is True:
            value += f"{bcolors.GREEN}"
        else:
            value += f"{bcolors.FAIL}"
        value += f"{str(v)}{bcolors.ENDC}"
    elif type(v) == int or type(v) == float:
        value = f"{bcolors.CYAN}{str(v)}{bcolors.ENDC}"
    elif type(v) == str:
        value = f"{bcolors.WARNING}'{str(v)}'{bcolors.ENDC}"
    elif v is None:
        value = f"{bcolors.FAIL}{str(v)}{bcolors.ENDC}"
    else:
        value = f"{v}"
    return value


def dump(obj, nested_level=0, output=sys.stdout, hex_to_int=False, debug=True, _is_list=False):
    """
    Print a variable for debugging.

    :param obj:
    :param nested_level:
    :param output:
    :param hex_to_int:
    :param debug:
    :param _is_list:
    :return:
    """
    spacing = '   '
    def_spacing = '   '

    if type(obj) == dict:
        if nested_level == 0 or _is_list:
            print('%s{' % (def_spacing + (nested_level) * spacing))
        else:
            print("{")
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                print(bcolors.OKGREEN + '%s%s: ' % (def_spacing + (nested_level + 1) * spacing, k) + bcolors.ENDC, end="")
                dump(v, nested_level + 1, output, hex_to_int, debug)
            else:
                if debug:
                    v = f"{get_colorful_object(v)} {bcolors.HEADER} {str(type(v)):>20}{bcolors.ENDC}{bcolors.DARK_GREY} len={len(str(v))}{bcolors.ENDC}"
                print(bcolors.OKGREEN + '%s%s:' % (def_spacing + (nested_level + 1) * spacing, k) + bcolors.WARNING + ' %s ' % v + bcolors.ENDC,
                      file=output)
        print('%s}' % (def_spacing + nested_level * spacing), file=output)
    elif type(obj) == list:
        print('%s[' % (def_spacing + (nested_level) * spacing), file=output)
        for v in obj:
            if hasattr(v, '__iter__'):
                dump(v, nested_level + 1, output, hex_to_int, debug, _is_list=True)
            else:
                print(bcolors.WARNING + '%s%s' % (def_spacing + (nested_level + 1) * spacing, get_colorful_object(v)) + bcolors.ENDC, file=output)
        print('%s]' % (def_spacing + (nested_level) * spacing), file=output)
    else:
        if debug:
            obj = f"{get_colorful_object(obj)} {bcolors.HEADER} {str(type(obj)):>20}{bcolors.ENDC}{bcolors.DARK_GREY} len={len(str(obj))}{bcolors.ENDC}"
        if hex_to_int and converter.is_hex(obj):
            print(bcolors.WARNING + '%s%s' % (def_spacing + nested_level * spacing, str(round(int(obj, 16) / 10 ** 18, 8)) + bcolors.ENDC))
        else:
            print(bcolors.WARNING + '%s%s' % (def_spacing + nested_level * spacing, obj) + bcolors.ENDC)
            # print(bcolors.WARNING + '%s' % (obj) + bcolors.ENDC)


def debug_print(text, color="green", on_color=None, attrs=None, view_time=True, **kwargs):
    """Print colorize text.

    It accepts arguments of print function.
    """
    module_name = ''
    stack = inspect.stack()
    parent_frame = stack[1][0]
    module = inspect.getmodule(parent_frame)
    if module:
        module_pieces = module.__name__.split('.')
        module_name = list_to_oneline_string(module_pieces)
    function_name = stack[1][3]
    full_module_name = f"{module_name}.{function_name}({stack[1].lineno})"

    module_text = ""
    time_text = ""
    try:
        # if global_verbose > 2:
            # text = f"[{full_module_name}] {text}"
        module_text = get_bcolors(f"[{full_module_name:<25}]", "WARNING")
    except:
        pass

    if view_time:
        time_text = "[" + get_bcolors(f"{date_utils.todaydate('log')}", "WHITE") + "]"
    main_text = (colored(str(text), color, on_color, attrs))
    print(f"{time_text}{module_text} {main_text}", **kwargs)


def classdump(obj):
    """
    For debugging, Print the properties of the class are shown.
    :param obj:
    :return:
    """
    for attr in dir(obj):
        if hasattr(obj, attr):
            value = getattr(obj, attr)
            print(bcolors.OKGREEN + f"obj.{attr} = " + bcolors.WARNING + f"{value}" + bcolors.ENDC)


def kvPrint(key, value, color="yellow"):
    """
    print the  {key: value} format.

    :param key:
    :param value:
    :param color:
    :return:
    """
    key_width = 9
    key_value = 3
    print(bcolors.OKGREEN + "{:>{key_width}} : ".format(key, key_width=key_width) + bcolors.ENDC, end="")
    print(bcolors.WARNING + "{:>{key_value}} ".format(str(value), key_value=key_value) + bcolors.ENDC)


def print_json(obj, **kwargs):
    """
    converted to JSON and print

    :param obj:
    :param kwargs:
    :return:
    """
    if isinstance(obj, dict) or isinstance(obj, list):
        print(json.dumps(obj, **kwargs))
    else:
        print(obj)


def debug_logging(message, dump_message=None, color="green"):
    """
    print debug_logging

    :param message:
    :param dump_message:
    :param color:
    :return:

    Example:

        .. code-block:: python

            from pawnlib import output

            output.debug_logging("message")

            [2022-07-25 16:35:15.105][DBG][/Users/jinwoo/work/python_prj/pawnlib/examples/asyncio/./run_async.py main(33)] : message

    """
    stack = traceback.extract_stack()
    filename, codeline, funcName, text = stack[-2]

    def_msg = f"[{date_utils.todaydate('log')}][DBG][{filename} {funcName}({codeline})]"
    kvPrint(def_msg, message)
    if dump_message:
        dump(dump_message)


def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, bar_length=100, overlay=True):
    """
    Print progress bar

    :param iteration:
    :param total:
    :param prefix:
    :param suffix:
    :param decimals:
    :param bar_length:
    :param overlay:
    :return:

    Example:

        from pawnlib import output

        .. code-block:: python

            for i in range(1, 100):
                time.sleep(0.05)
                output.print_progress_bar(i, total=100, prefix="start", suffix="suffix")

            # >> start |\#\#\#\#\#\#\#\| 100.0% suffix

    """
    iteration = iteration + 1
    format_str = "{0:." + str(decimals) + "f}"
    percent = format_str.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '#' * filled_length + '-' * (bar_length - filled_length)

    if overlay:
        sys.stdout.write("\033[F")  # back to previous line
        sys.stdout.write("\033[K")  # clear line
    sys.stdout.write('%s |%s| %s%s %s \n' %
                     (prefix, bar, percent, '%', suffix)),

    if iteration == total:
        sys.stdout.write('\n')
    # sys.stdout.flush()


# def run_progress():
#     animation = ["\\", "|", " /", "—"]

