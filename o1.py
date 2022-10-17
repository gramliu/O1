import argparse
import subprocess
from src.get_commands import get_commands

# Configure root and subparsers
parser = argparse.ArgumentParser(description="Run predefined commands")
subparsers = parser.add_subparsers(dest="action", description="Action to run")
list_parser = subparsers.add_parser(
    "list", description="List available commands")
run_parser = subparsers.add_parser("run", description="Run a command")

# Load command parsers
commands = get_commands()
run_subparsers = run_parser.add_subparsers(
    dest="command", description="Command to run")
for command_name in commands.keys():
    command = commands[command_name]

    examples = "\n".join(
        map(lambda example: f"o1 run {example}", command.examples))
    cmd_parser = run_subparsers.add_parser(
        command_name, description=f"{command.description}", usage=examples)

    cli_args = command.get_arguments()
    for arg in cli_args:
        cmd_parser.add_argument(
            f"--{arg.name}", f"-{arg.alias}", help=arg.description, required=arg.required)

cli_args = parser.parse_args()

if cli_args.action == "list":
    # Display available commands
    print("="*20)
    print("Available commands:")
    print("="*20)
    for alias in commands:
        command = commands[alias]
        print(alias, command.name, sep="\t\t")
elif cli_args.action == "run":
    # Execute the specified command
    command_name = cli_args.command
    if command_name not in commands:
        raise ValueError(f"Unknown command: {command_name}")

    command = commands[command_name]
    cmd_args = command.get_arguments()
    arg_values = []
    for cmd_arg in cmd_args:
        if cmd_arg.name in cli_args:
            arg_values.append(cli_args.__getattribute__(cmd_arg.name))
    subprocess.run([command.program, f"scripts/{command.source}"] + arg_values)
