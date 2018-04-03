import sys
import argparse

COMMANDS = ("add", "chat", "file")

INDENT = " " * 2
NEWLINE = "\n" + INDENT


def command_error():
    usage = NEWLINE + "%(prog)s <command> [parameters]\n\n" \
        + "Valid commands are:\n\n" \
        + INDENT + NEWLINE.join(COMMANDS)

    parser = argparse.ArgumentParser(
        prog="stalk",
        usage=usage,
    )
    parser.print_help()
    sys.exit(-1)


def check_argument(args):
    command = args[1]

    if command not in COMMANDS:
        command_error()


def get_command(command):
    if command in COMMANDS:
        return globals()[command.capitalize() + "Command"]
    else:
        command_error()


def main():
    args = sys.argv
    check_argument(args)
    command = get_command(args[1])
    command.main(args[2:])
