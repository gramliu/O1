import os
from typing import Mapping
import yaml

CMD_DIR = "./commands"

ext_map = {
    "bash": "sh",
    "python": "py"
}


class Command:
    """
    Command wraps an executable script and its associated metadata
    """

    def __init__(self, name: str, description: str, program: str, script: str):
        self.name = name
        self.description = description
        self.program = program
        self.script = script


def get_commands() -> Mapping[str, Command]:
    """
    Returns the available commands 
    """
    commands = {}
    for fn in os.listdir(CMD_DIR):
        base_name = os.path.splitext(fn)[0]
        with open(os.path.join(CMD_DIR, fn), "r") as file:
            command = yaml.load(file.read(), Loader=yaml.CLoader)
            ext = ext_map[command["program"]]
            matches = command["matches"]

            for match in matches:
                commands[match] = {
                    "name": command["name"],
                    "description": command["description"],
                    "program": command["program"],
                    "script": f"{base_name}.{ext}",
                }
    return commands
