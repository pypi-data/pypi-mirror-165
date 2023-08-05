#!/bin/sh

##############################################################################
# BOOTSTRAP
#
# Include ../lib in the search path so we can find termwriter when running locally
# then call python3 or python, whichever exists.
# (See https://unix.stackexchange.com/questions/20880)
#
if "true" : '''\'
then
    export PYTHONPATH="$(dirname $0)/../lib:$PYTHONPATH"
    pythoncmd=python

    if command -v python3 >/dev/null; then
        pythoncmd=python3
    fi

    exec "$pythoncmd" "$0" "$@"
    exit 127
fi
'''

##############################################################################
# PYTHON CODE BEGINS HERE

__copyright__ = "Copyright 2019-2022 Mark Kim"
__license__ = "Apache 2.0"
__version__ = "1.0.0"
__author__ = "Mark Kim"

import sys
import errno
from termwriter import Screen
from termwriter import TextBox
from termwriter import Table

with Screen('My Screen') as screen:
    with screen.section('My First Box', Table('l')) as box:
        with box.draw(TextBox()) as tbox:
            tbox.write('I can nest boxes.\n')
            tbox.write('Below is a table:\n')

        with box.draw(Table('ll')) as table:
            table.write('Name:', 'John Q. Public')
            table.write('Tel:', '+1 111 555 3333')
            table.write('Email:', 'nobody@nowhere.com')


# vim:filetype=python:
