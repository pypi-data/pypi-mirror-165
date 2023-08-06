

from abc import ABC, abstractmethod
from typing import Optional
from galaxy.tool_util.parser.output_objects import ToolOutput as GxOutput

from ..param.ParamRegister import ParamRegister
from ..param.OutputParam import (
    OutputParam,
    DataOutputParam,
    CollectionOutputParam,
)

from galaxy2janis import expressions
from galaxy2janis.expressions.patterns import WILDCARD_GROUP


class Factory(ABC):
    @abstractmethod
    def create(self, gxout: GxOutput, inputs: ParamRegister)  -> OutputParam:
        """parses galaxy output to return an OutputParam"""
        ...

class DataOutputFactory(Factory):
    def create(self, gxout: GxOutput, inputs: ParamRegister)  -> OutputParam:
        param = DataOutputParam(gxout.name)
        param.label = str(gxout.label).rsplit('}', 1)[-1].strip(': ')
        param.formats = fetch_format(gxout, inputs)
        param.from_work_dir = get_from_workdir_pattern(gxout)
        param.discover_pattern = get_discover_pattern(gxout)
        return param

class CollectionOutputFactory(Factory):
    def create(self, gxout: GxOutput, inputs: ParamRegister)  -> OutputParam:
        param = CollectionOutputParam(gxout.name)
        param.label = str(gxout.label).rsplit('}', 1)[-1].strip(': ')
        if gxout.structure.collection_type != '':
            param.collection_type = str(gxout.structure.collection_type) 
        param.formats = fetch_format(gxout, inputs)
        param.discover_pattern = get_discover_pattern(gxout)
        return param


def get_from_workdir_pattern(gxout: GxOutput) -> Optional[str]:
    if has_from_workdir(gxout):
        return gxout.from_work_dir
    return None

def get_discover_pattern(gxout: GxOutput) -> Optional[str]:
    if has_dataset_collector(gxout):
        collector = gxout.dataset_collector_descriptions[0]
        pattern = f'{collector.directory}/{collector.pattern}' # type: ignore
        return remove_pattern_capture_groups(pattern)
    return None

def remove_pattern_capture_groups(pattern: str) -> str:
    matches = expressions.get_matches(pattern, WILDCARD_GROUP)
    for m in matches:
        pattern = pattern.replace(m.group(0), m.group(2))
    return pattern



factory_map = {
    'data': DataOutputFactory,
    'float': DataOutputFactory,
    'collection': CollectionOutputFactory
}

def parse_output_param(gxout: GxOutput, inputs: ParamRegister) -> list[OutputParam]:
    galaxy_params: list[GxOutput] = []
    internal_params: list[OutputParam] = []

    # split collection of defined outputs to list 
    if is_defined_collection(gxout):
        for g_param in gxout.outputs.values(): # type: ignore
            galaxy_params.append(g_param)
    # parse the output as usual
    else:
        galaxy_params.append(gxout)
    
    for g_param in galaxy_params:
        f_class = factory_map[g_param.output_type]
        factory = f_class()
        i_param = factory.create(g_param, inputs)
        internal_params.append(i_param)
    return internal_params

def is_defined_collection(gxout: GxOutput) -> bool:
    if hasattr(gxout, 'outputs') and len(gxout.outputs) > 0:  # type: ignore
        return True
    return False


def fetch_format(gxout: GxOutput, inputs: ParamRegister) -> list[str]:
    strategy: FetchStrategy = select_fetcher(gxout)
    return strategy.fetch(gxout, inputs)

def has_format(gxout: GxOutput) -> bool:
    if hasattr(gxout, 'format'):
        if gxout.format and gxout.format != 'data':
            return True
    return False

def has_default_format(gxout: GxOutput) -> bool:
    if hasattr(gxout, 'default_format'): 
        if gxout.default_format and gxout.default_format != 'data':
            return True
    return False

def has_format_source(gxout: GxOutput) -> bool:
    if hasattr(gxout, 'format_source'):
        if gxout.format_source:
            return True
    return False

def has_from_workdir(gxout: GxOutput) -> bool:
    if gxout.output_type == 'data': # type: ignore
        if hasattr(gxout, 'from_work_dir') and gxout.from_work_dir: # type: ignore
            return True
    return False

def has_dataset_collector(gxout: GxOutput) -> bool:
    if hasattr(gxout, 'dynamic_structure') and gxout.dynamic_structure: # type: ignore
        if hasattr(gxout, 'dataset_collector_descriptions'):
            return True
    return False

# helper classes 
class FetchStrategy(ABC):
    @abstractmethod
    def fetch(self, gxout: GxOutput, inputs: ParamRegister) -> list[str]:
        """gets the galaxy datatype formats for this galaxy output"""
        ...

class FormatFetchStrategy(FetchStrategy):
    def fetch(self, gxout: GxOutput, inputs: ParamRegister) -> list[str]:
        return str(gxout.format).split(',')

class DefaultFormatFetchStrategy(FetchStrategy):
    def fetch(self, gxout: GxOutput, inputs: ParamRegister) -> list[str]:
        return str(gxout.default_format).split(',')

class FormatSourceFetchStrategy(FetchStrategy):
    def fetch(self, gxout: GxOutput, inputs: ParamRegister) -> list[str]:
        param = inputs.get(gxout.format_source, strategy='lca')
        if param:
            return param.formats
        return []

class CollectorFetchStrategy(FetchStrategy):
    def fetch(self, gxout: GxOutput, inputs: ParamRegister) -> list[str]:
        coll = gxout.dataset_collector_descriptions[0]
        if coll.default_ext:
            return str(coll.default_ext).split(',')
        return []

class FallbackFetchStrategy(FetchStrategy):
    def fetch(self, gxout: GxOutput, inputs: ParamRegister) -> list[str]:
        return []

def select_fetcher(gxout: GxOutput) -> FetchStrategy:
    if has_format(gxout):
        return FormatFetchStrategy()
    elif has_default_format(gxout):
        return DefaultFormatFetchStrategy()
    elif has_format_source(gxout):
        return FormatSourceFetchStrategy()
    elif has_dataset_collector(gxout):
        return CollectorFetchStrategy()
    else:
        return FallbackFetchStrategy()







