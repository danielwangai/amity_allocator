#!/usr/bin/env python
"""
This example uses docopt with the built in cmd module to demonstrate an
interactive command application.
Usage:
    amity create_room (living_space|office) <name>...
    amity add_person (Fellow|Staff) <first_name> <last_name> <wants_accomodation>
    amity print_unallocated_to_office
    amity print_room <room_name>
    amity print_unallocated_living_space
    amity print_office_allocations
    amity (-i | --interactive)
    amity (-h | --help | --version)
Options:
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
    --baud=<n>  Baudrate [default: 9600]
"""

import sys
import cmd
from docopt import docopt, DocoptExit
from app import amity


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


class Amity(cmd.Cmd):

    def intro():
        print('------------------------------------------------------------------------------')
        print('------------------------------------------------------------------------------')

    intro = intro()
    prompt = '(Amity) '
    file = None

    @docopt_cmd
    def do_create_room(self, args):
        """Usage: create_room (living_space|office) <name>..."""
        amity.create_room(args)

    @docopt_cmd
    def do_add_person(self, args):
        """Usage: add_person (Fellow|Staff) <first_name> <last_name> <wants_accomodation>"""
        amity.add_person(args)

    @docopt_cmd
    def do_print_unallocated_to_office(self, args):
        """Usage: print_unallocated_to_office"""
        amity.print_unallocated_to_office()

    @docopt_cmd
    def do_print_room(self, args):
        """Usage: print_room <room_name>"""
        amity.print_room(args)

    @docopt_cmd
    def do_print_unallocated_living_space(self, args):
        """Usage: print_unallocated_living_space"""
        amity.print_fellows_unallocated_to_living_space()

    @docopt_cmd
    def do_print_office_allocations(self, args):
        """Usage: print_office_allocations"""
        amity.print_office_allocations()

    def do_quit(self, arg):
        """Quits out of Interactive Mode."""

        print('Good Bye!')
        exit()


opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']:
    Amity().cmdloop()

print(opt)
