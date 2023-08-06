

from __future__ import annotations
from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from galaxy2janis.entities.tool.Tool import Tool
    from galaxy2janis.entities.workflow import Workflow
    from galaxy2janis.entities.workflow import WorkflowInput
    from galaxy2janis.entities.workflow import WorkflowStep
    from galaxy2janis.entities.workflow import StepOutput

    from galaxy2janis.gx.command.components import InputComponent
    from galaxy2janis.gx.command.components import OutputComponent


# split this file into mapping.workflow, mapping.tool?

def tool_input(galaxy_param_name: str, tool: Tool) -> Optional[InputComponent]:
    """given a galaxy param name, get the corresponding Tool InputComponent if exists"""
    for inp in tool.inputs:
        if inp.gxparam and inp.gxparam.name == galaxy_param_name:
            return inp

def tool_output(galaxy_param_name: str, tool: Tool) -> Optional[OutputComponent]:
    """given a galaxy param name, get the corresponding Tool OutputComponent if exists"""
    for out in tool.outputs:
        if out.gxparam and out.gxparam.name == galaxy_param_name:
            return out

def emitter(query_id: str, query_output: str, janis: Workflow, galaxy: dict[str, Any]) -> StepOutput | WorkflowInput:
    """given a galaxy step id and output name, get the corresponding janis StepOutput or WorkflowInput"""
    g_step = _get_galaxy_step(query_id, galaxy)
    if g_step['type'] == 'tool':
        j_step = step(g_step['id'], janis, galaxy)
        return _get_janis_step_output(query_output, j_step, g_step)
    else:
        return _get_janis_w_input(g_step['id'], janis, galaxy)

def step(query_id: str, janis: Workflow, galaxy: dict[str, Any]) -> WorkflowStep:
    """lookup the corresponding janis step for a galaxy step with id=query_id"""
    g_step = _get_galaxy_step(query_id, galaxy)
    if 'janis_uuid' not in g_step:
        raise RuntimeError('Galaxy step not linked to janis step')
    janis_step_uuid = g_step['janis_uuid']
    return _get_janis_step(janis_step_uuid, janis)

def _get_galaxy_step(query_id: str, galaxy: dict[str, Any]) -> dict[str, Any]:
    for step in galaxy['steps'].values():
        if step['id'] == query_id:
            return step
    raise RuntimeError(f'No galaxy step with id {query_id}')

def _get_janis_step(query_uuid: str, janis: Workflow) -> WorkflowStep:
    for step in janis.steps:
        if step.uuid == query_uuid:
            return step
    raise RuntimeError(f'No janis step with uuid {query_uuid}')

def _get_janis_step_output(query_output: str, j_step: WorkflowStep, g_step: dict[str, Any]) -> StepOutput:
    """sorry"""
    j_outs = j_step.outputs.list()
    g_outs = g_step['outputs']
    for out in g_outs:
        if out['name'] == query_output:
            for output in j_outs:
                if output.uuid == out['janis_uuid']:
                    return output
    raise RuntimeError(f'No janis step output for galaxy step output {query_output}')

def _get_janis_w_input(query_id: str, janis: Workflow, galaxy: dict[str, Any]) -> WorkflowInput:
    g_step = _get_galaxy_step(query_id, galaxy)
    for inp in janis.inputs:
        if inp.uuid == g_step['janis_uuid']:
            return inp
    raise RuntimeError(f'No janis workflow input with uuid {query_id}')



