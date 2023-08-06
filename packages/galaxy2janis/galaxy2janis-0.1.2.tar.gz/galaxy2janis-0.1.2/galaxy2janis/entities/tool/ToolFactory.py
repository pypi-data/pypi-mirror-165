

from galaxy2janis.logs import logging
from galaxy2janis.gx.gxtool import XMLToolDefinition
from galaxy2janis.gx.command import Command
from typing import Optional

# this module imports
from .Tool import Tool
from .outputs import extract_outputs


class ToolFactory:
    def __init__(self, xmltool: XMLToolDefinition, command: Command, container: Optional[str]) -> None:
        self.xmltool = xmltool
        self.command = command
        self.container = container

    def create(self) -> Tool:
        tool = Tool(
            metadata=self.xmltool.metadata,
            container=self.container,
            base_command=self.get_base_command(),
            gxparam_register=self.xmltool.inputs,
            configfiles=self.xmltool.configfiles
        )
        self.supply_inputs(tool)
        self.supply_outputs(tool)
        return tool

    def supply_inputs(self, tool: Tool) -> None:
        self.command.set_cmd_positions()
        inputs = self.command.list_inputs(include_base_cmd=False)
        if not inputs:
            logging.no_inputs()
        for inp in inputs:
            tool.add_input(inp)

    def supply_outputs(self, tool: Tool) -> None:
        outputs = extract_outputs(self.xmltool, self.command)
        if not outputs:
            logging.no_outputs()
        for out in outputs:
            tool.add_output(out)

    def get_base_command(self) -> list[str]:
        positionals = self.command.get_base_positionals()
        if not positionals:
            logging.no_base_cmd()
        return [p.default_value for p in positionals]
    