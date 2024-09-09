from typing import List
import os
from concurrent.futures import ProcessPoolExecutor

from gaussianinputleaflet import GaussianInputLeaflet
from gaussianoutputleaflet import GaussianOutputLeaflet
from node import Node
import num_generating_processes as ngp

class Branch:
    def __init__(self, dirpath: str):
        self.path: str = dirpath
        num_executors: int = round(len(self.get_subdirs()) / ngp.BRANCH_EXECUTOR_DIVISOR)
        if num_executors < 1: num_executors = 1
        with ProcessPoolExecutor(num_executors) as p:
            self.nodes: List[Node] = [node for node in p.map(Node, self.get_subdirs())]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(path:{self.path},nodes:{self.nodes})"
    
    def get_subdirs(self) -> List[str]:
        subdirpaths: List[str] = list()
        for root, dirs, files in os.walk(self.path):
            subdirpaths.extend([os.path.join(root, dirname) for dirname in dirs])
        return subdirpaths
    
    def get_incomplete_gaussian_outputs(self) -> List[GaussianOutputLeaflet]:
        incomplete_outputs: List[GaussianOutputLeaflet] = list()
        for node in self.nodes:
            incomplete_outputs.extend(node.get_incomplete_gaussian_outputs())
        return incomplete_outputs

    def get_unrun_gaussian_inputs(self) -> List[GaussianInputLeaflet]:
        unrun_inputs: List[GaussianInputLeaflet] = list()
        for node in self.nodes:
            unrun_inputs.extend(node.get_unrun_gaussian_inputs())
        return unrun_inputs

    def get_gaussian_inputs_to_rerun(self) -> List[GaussianInputLeaflet]:
        inputs_to_rerun: List[GaussianInputLeaflet] = list()
        for node in self.nodes:
            inputs_to_rerun.extend(node.get_gaussian_inputs_to_rerun())
        return inputs_to_rerun
