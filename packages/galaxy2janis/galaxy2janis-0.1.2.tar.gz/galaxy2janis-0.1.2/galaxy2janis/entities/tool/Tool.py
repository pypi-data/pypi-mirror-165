



from dataclasses import dataclass
from typing import Optional
from uuid import uuid4

from galaxy2janis import tags
from galaxy2janis.gx.configfiles.Configfile import Configfile
from galaxy2janis.gx.gxtool import ToolXMLMetadata
from galaxy2janis.gx.gxtool.param import ParamRegister
from galaxy2janis.gx.gxtool.param import Param
from galaxy2janis.gx.command.components import CommandComponent
from galaxy2janis.gx.command.components import InputComponent
from galaxy2janis.gx.command.components import OutputComponent


# shouldn't really be a dataclass, just annoying to write __init__ method
@dataclass
class Tool:
    """
    a Tool() is the final representation of the software tool
    a galaxy XML wrapper is running. Includes metadata, inputs, outputs, a container to execute the tool, base command etc. 
    """
    metadata: ToolXMLMetadata
    gxparam_register: ParamRegister
    configfiles: list[Configfile]
    container: Optional[str]
    base_command: list[str]

    def __post_init__(self):
        self.inputs: list[InputComponent] = []
        self.outputs: list[OutputComponent] = []
        self.uuid: str = str(uuid4())
        tags.new_group('tool', self.uuid)
        tags.register(self)

    @property
    def name(self) -> str:
        return self.metadata.id
    
    @property
    def tag(self) -> str:
        return tags.get(self.uuid)

    def add_input(self, inp: InputComponent) -> None:
        tags.switch_group(self.uuid)
        tags.register(inp)
        self.inputs.append(inp)
    
    def add_output(self, out: OutputComponent) -> None:
        tags.switch_group(self.uuid)
        tags.register(out)
        self.outputs.append(out)

    def get_gxparam(self, query: str) -> Optional[Param]:
        param = self.gxparam_register.get(query, strategy='lca')
        if not param:
            pass
            #raise RuntimeError(f'no gxparam named {query}')
        return param
   
    def get_input(self, query_uuid: str) -> Optional[CommandComponent]:
        for inp in self.inputs:
            if query_uuid == inp.uuid:
                return inp
        raise RuntimeError(f'could not find {query_uuid} in tool inputs')
    
    def get_input_via_param_name(self, query_uuid: str) -> CommandComponent:
        for inp in self.inputs:
            if query_uuid == inp.uuid:
                return inp
        raise RuntimeError(f'could not find {query_uuid} in tool inputs')

    def get_preprocessing(self) -> Optional[str]:
        raise NotImplementedError

    def get_postprocessing(self) -> Optional[str]:
        raise NotImplementedError



    
