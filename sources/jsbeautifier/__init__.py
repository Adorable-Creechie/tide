from __future__ import print_function
import sys
import os
import platform
import io
import getopt
import re
import string
import errno
import copy
import glob
import __version__
from javascript.options import BeautifierOptions
from javascript.beautifier import Beautifier

#
# The MIT License (MIT)

# Copyright (c) 2007-2018 Einar Lielmanis, Liam Newman, and contributors.

# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Originally written by Einar Lielmanis et al.,
# Conversion to python by Einar Lielmanis, einar@beautifier.io,
# Parsing improvement for brace-less and semicolon-less statements
#    by Liam Newman <bitwiseman@beautifier.io>
# Python is not my native language, feel free to push things around.
#
# Use either from command line (script displays its usage when run
# without any parameters),
#
#
# or, alternatively, use it as a module:
#
#   import jsbeautifier
#   res = jsbeautifier.beautify('your javascript string')
#   res = jsbeautifier.beautify_file('some_file.js')
#
#  you may specify some options:
#
#   opts = jsbeautifier.default_options()
#   opts.indent_size = 2
#   res = jsbeautifier.beautify('some javascript', opts)
#
#
# Here are the available options: (read source)


class MissingInputStreamError(Exception):
    pass

def default_options():
    return BeautifierOptions()


def beautify(string, opts=default_options()):
    b = Beautifier()
    return b.beautify(string, opts)


def set_file_editorconfig_opts(filename, js_options):
    from editorconfig import get_properties, EditorConfigError
    try:
        _ecoptions = get_properties(os.path.abspath(filename))

        if _ecoptions.get("indent_style") == "tab":
            js_options.indent_with_tabs = True
        elif _ecoptions.get("indent_style") == "space":
            js_options.indent_with_tabs = False

        if _ecoptions.get("indent_size"):
            js_options.indent_size = int(_ecoptions["indent_size"])

        if _ecoptions.get("max_line_length"):
            if _ecoptions.get("max_line_length") == "off":
                js_options.wrap_line_length = 0
            else:
                js_options.wrap_line_length = int(
                    _ecoptions["max_line_length"])

        if _ecoptions.get("insert_final_newline") == 'true':
            js_options.end_with_newline = True
        elif _ecoptions.get("insert_final_newline") == 'false':
            js_options.end_with_newline = False

        if _ecoptions.get("end_of_line"):
            if _ecoptions["end_of_line"] == "cr":
                js_options.eol = '\r'
            elif _ecoptions["end_of_line"] == "lf":
                js_options.eol = '\n'
            elif _ecoptions["end_of_line"] == "crlf":
                js_options.eol = '\r\n'

    except EditorConfigError:
        # do not error on bad editor config
        print("Error loading EditorConfig.  Ignoring.", file=sys.stderr)

def beautify_file(file_name, opts=default_options()):
    input_string = ''
    if file_name == '-':  # stdin
        if sys.stdin.isatty():
            raise MissingInputStreamError()

        stream = sys.stdin
        if platform.platform().lower().startswith('windows'):
            if sys.version_info.major >= 3:
                # for python 3 on windows this prevents conversion
                stream = io.TextIOWrapper(sys.stdin.buffer, newline='')
            elif platform.architecture()[0] == '32bit':
                # for python 2 x86 on windows this prevents conversion
                import msvcrt
                msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
            else:
                raise Exception('Pipe to stdin not supported on Windows with Python 2.x 64-bit.')

        input_string = stream.read()

        # if you pipe an empty string, that is a failure
        if input_string == '':
            raise MissingInputStreamError()
    else:
        stream = io.open(file_name, 'rt', newline='', encoding='UTF-8')
        input_string = stream.read()

    return beautify(input_string, opts)


def mkdir_p(path):
    try:
        if path:
            os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise Exception()


def isFileDifferent(filepath, expected):
    try:
        return (
            ''.join(
                io.open(
                    filepath,
                    'rt',
                    newline='').readlines()) != expected)
    except BaseException:
        return True
