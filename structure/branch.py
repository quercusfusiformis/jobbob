from pathlib import Path
from concurrent.futures import ProcessPoolExecutor

import num_generating_processes as ngp
from node import Node
from gaussianinputleaflet import GaussianInputLeaflet
from gaussianoutputleaflet import GaussianOutputLeaflet
from orcainputleaflet import OrcaInputLeaflet
from orcaoutputleaflet import OrcaOutputLeaflet

class Branch:
    def __init__(self, pathstr: str):
        self.path: Path = Path(pathstr)
        subdirs: tuple[Path] = self.get_subdirs()
        num_executors: int = round(len(subdirs) / ngp.BRANCH_EXECUTOR_DIVISOR)
        if num_executors < 1:
            num_executors = 1
        elif num_executors > 61:
            num_executors = 61
        with ProcessPoolExecutor(num_executors) as p:
            self.nodes: tuple[Node] = tuple(node for node in p.map(Node, subdirs))
        # self.nodes: tuple[Node] = tuple(Node(pathstr=str(subdir)) for subdir in subdirs)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(path:{self.path},nodes:{self.nodes})"
    
    def get_subdirs(self) -> tuple[Path]:
        subdir_paths: list[Path] = list()
        for path, dirnames, filenames in self.path.walk():
            subdir_paths.extend(tuple(path.joinpath(dirname) for dirname in dirnames))
        return tuple(subdir_paths)
    
    def get_incomplete_gaussian_outputs(self) -> tuple[GaussianOutputLeaflet]:
        incomplete_outputs: list[GaussianOutputLeaflet] = list()
        for node in self.nodes:
            incomplete_outputs.extend(node.get_incomplete_gaussian_outputs())
        return tuple(incomplete_outputs)

    def get_unrun_gaussian_inputs(self) -> tuple[GaussianInputLeaflet]:
        unrun_inputs: list[GaussianInputLeaflet] = list()
        for node in self.nodes:
            unrun_inputs.extend(node.get_unrun_gaussian_inputs())
        return tuple(unrun_inputs)
