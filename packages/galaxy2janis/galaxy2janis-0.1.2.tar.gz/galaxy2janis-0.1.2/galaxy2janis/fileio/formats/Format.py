

from abc import ABC, abstractmethod

from galaxy2janis.entities.tool import Tool
from galaxy2janis.entities.workflow import Workflow
from galaxy2janis.entities.workflow import WorkflowStep


class Format(ABC):
    """
    controls the format of pages user will see.
    example 1: controls whether the workflow steps will be 
    broken into subworkflows or not. 
    example 2?: controls which workflows will have an inputs dict file created? 
    """

    @abstractmethod
    def workflow(self, workflow: Workflow) -> str:
        """returns the workflow page"""
        ...
    
    @abstractmethod
    def subworkflow(self, workflow: Workflow) -> str:
        """returns a subworkflow"""
        ...
    
    @abstractmethod
    def step(self, step: WorkflowStep) -> str:
        """writes a step"""
        ...

    @abstractmethod
    def tool(self, tool: Tool) -> str:
        """writes a tool"""
        ...

    @abstractmethod
    def script(self) -> str:
        """writes a script used with a tool"""
        ...
    
    @abstractmethod
    def inputs(self, workflow: Workflow) -> str:
        """writes the workflow inputs file"""
        ...
    
    @abstractmethod
    def config(self, workflow: Workflow) -> str:
        """writes the workflow config file"""
        ...


