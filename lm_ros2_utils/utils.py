import argparse
import sys


def parse_launch_arguments():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("command")
    parser.add_argument("package")
    parser.add_argument("file")
    parser.add_argument("arguments", nargs='*')

    return parser.parse_args()


def build_arguments_dict(arguments):
    arg_dict = {}

    for arg in arguments:
        argument_name, value = arg.split(":=")

        if value == None:
            print("Cannot read value of argument", argument_name, " Please use: <argument_name>:=<value>")
            sys.exit(1)
    
        arg_dict[argument_name] = value

    return arg_dict
