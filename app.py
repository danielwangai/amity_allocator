"""#!/usr/bin/env python .

This example uses docopt with the built in cmd module to demonstrate an
interactive command application.
Usage:
    amity create_room (living_space|office) <room_name>...
    amity add_person (Fellow|Staff) <first_name> <last_name> [--accomodation=value]
    amity print_room <room_name>
    amity print_unallocated [--file=text_file]
    amity print_allocations [--file=text_file]
    amity reallocate_person <person_id> <new_room>
    amity save_state [--db=sqlite_database]
    amity load_state <db>
    amity load_state <text_file>
    amity print_all_rooms
    amity print_all_people
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
from pyfiglet import figlet_format
from termcolor import cprint

from app import amity


def docopt_cmd(func):
    """To provide a decorator used to simplify the try/except block.

    and pass the result of the docopt parsing to the called action.

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
    """Define contain methods/commands for docopt interface on terminal."""

    def intro():
        """Contain introductory message when in interactive mode."""
        cprint(figlet_format("Amity", font="univers"), "blue")

    intro = intro()
    prompt = '(Amity) '
    file = None

    @docopt_cmd
    def do_create_room(self, args):
        """Usage: create_room (living_space|office) <room_name>..."""
        room_type = None
        if args["office"]:
            room_type = "office"
        else:
            room_type = "living_space"
        print(args["<room_name>"])

        amity.create_room(room_type, args["<room_name>"])

    @docopt_cmd
    def do_add_person(self, args):
        """Usage: add_person (Fellow|Staff) <first_name> <last_name> [--accomodation=value]"""
        person_type = None
        if args["Fellow"]:
            person_type = "Fellow"
        else:
            person_type = "Staff"
        first_name = args["<first_name>"]
        last_name = args["<last_name>"]
        amity.add_person(person_type, first_name,
                         last_name, args["--accomodation"])

    @docopt_cmd
    def do_print_room(self, args):
        """Usage: print_room <room_name>"""
        room_name = args["<room_name>"]
        amity.print_room(room_name)

    @docopt_cmd
    def do_print_unallocated(self, args):
        """Usage: print_unallocated [--file=text_file]"""
        amity.print_unallocated(args['--file'])

    @docopt_cmd
    def do_print_allocations(self, args):
        """Usage: print_allocations [--file=text_file]"""
        amity.print_allocations(args["--file"])

    @docopt_cmd
    def do_reallocate_person(self, args):
        """Usage: reallocate_person <person_id> <new_room>"""
        if args["<person_id>"].isalpha():
            print("person id cannot be string")
            return
        else:
            (amity.reallocate_person(int(args['<person_id>']),
                                     args['<new_room>']))

    @docopt_cmd
    def do_save_state(self, args):
        """Usage: save_state [--db=sqlite_database]"""
        # print(args['--db'])
        amity.save_state(args['--db'])

    @docopt_cmd
    def do_load_state(self, args):
        """Usage: load_state <db>"""
        db_name = args["<db>"]
        amity.load_state(db_name)

    @docopt_cmd
    def do_load_people(self, args):
        """Usage: load_state <text_file>"""
        amity.load_people(args["<text_file>"])

    @docopt_cmd
    def do_print_all_rooms(self, arg):
        """Usage: print_all_rooms"""
        amity.print_all_rooms()

    @docopt_cmd
    def do_print_all_people(self, arg):
        """Usage: print_all_people"""
        amity.print_all_people()

    def do_quit(self, arg):
        """Quits out of Interactive Mode."""

        print('Good Bye!')
        exit()


opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']:
    Amity().cmdloop()

print(opt)
