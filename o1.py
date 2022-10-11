import argparse
from src.get_commands import get_commands

parser = argparse.ArgumentParser(description="Run predefined commands")
parser.add_argument("-l", "--list", action="store_true",
                    help="List available commands")

args = parser.parse_args()
if args.list:
    commands = get_commands()
    print("="*20)
    print("Available commands:")
    print("="*20)
    for alias in commands:
        command = commands[alias]
        print(alias, command["name"], sep="\t\t")
