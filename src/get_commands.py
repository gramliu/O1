from dataclasses import dataclass
import os
from typing import Generic, List, Mapping, Optional, TypeVar, Union
import yaml

CMD_DIR = "./commands"

ext_map = {
    "bash": "sh",
    "python": "py"
}

T = TypeVar("T")


@dataclass
class CommandArgument:
    """
    CommandArgument represents a single argument expected by a command.
    This includes the name of the argument, its type, and whether or not it is required
    """

    name: str
    description: Optional[str]
    required: bool
    alias: str


@dataclass
class Command:
    """
    Command wraps an executable script and its associated metadata
    """

    name: str
    description: str
    program: str  # Executable to run the script
    source: str  # Path to source script
    examples: List[str]
    _args: Optional[Mapping[str, CommandArgument]] = None

    def add_argument(self, argument: CommandArgument):
        """
        Add an argument to this command
        """
        if self._args is None:
            self._args = {}
        name = argument.name
        self._args[name] = argument

    def get_arguments(self) -> List[CommandArgument]:
        """
        Returns a list of arguments to be used with this command
        """
        if self._args is None:
            self._args = {}
        return sorted(self._args.values(), key=lambda command: command.name)


def get_commands() -> Mapping[str, Command]:
    """
    Returns the available commands 
    """
    commands = {}
    for fn in os.listdir(CMD_DIR):
        base_name = os.path.splitext(fn)[0]
        with open(os.path.join(CMD_DIR, fn), "r") as file:
            command_yaml = yaml.load(file.read(), Loader=yaml.CLoader)
            ext = ext_map[command_yaml["program"]]
            matches = command_yaml["matches"]

            # Initialize the command
            command = Command(
                name=command_yaml["name"],
                description=command_yaml["description"],
                program=command_yaml["program"],
                source=f"{base_name}.{ext}",
                examples=command_yaml["examples"]
            )

            # Populate the arguments
            for arg_name in command_yaml["args"]:
                arg_yaml = command_yaml["args"][arg_name]
                argument = CommandArgument(
                    name=arg_name,
                    description=arg_yaml["description"],
                    alias=arg_yaml["alias"],
                    required=arg_yaml["required"]
                )
                command.add_argument(argument)

            # Populate all matches in the command map
            for match in matches:
                commands[match] = command
    return commands
