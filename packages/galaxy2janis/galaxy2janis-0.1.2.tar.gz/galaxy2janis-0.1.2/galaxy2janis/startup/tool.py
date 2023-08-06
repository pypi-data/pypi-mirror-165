

from typing import Optional
from galaxy2janis.logs import logging
from galaxy2janis import settings
from galaxy2janis.utils import galaxy as utils


def tool_setup(args: dict[str, Optional[str]]) -> None:
    settings.tool.set(from_args=args)
    logging.msg_parsing_tool()
    validate_tool_settings()


### VALIDATION ###

def validate_tool_settings() -> None:
    # both local & remote params not given
    if not _has_xml() or not _valid_xml():
        raise RuntimeError('no valid xml file')

def _has_xml() -> bool:
    if settings.tool.tool_path:
        return True
    return False

def _valid_xml() -> bool:
    path = settings.tool.tool_path
    if utils.is_tool_xml(path):
        return True
    return False


