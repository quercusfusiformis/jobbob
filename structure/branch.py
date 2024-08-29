from typing import List
import os
from concurrent.futures import ProcessPoolExecutor

from comleaflet import ComLeaflet
from logleaflet import LogLeaflet
from node import Node
import num_generating_processes as ngp

class Branch:
    def __init__(self, dirpath: str):
        self.path: str = dirpath
        with ProcessPoolExecutor(ngp.NODE_GENERATING_PROCESSES) as p:
            self.nodes: List[Node] = [node for node in p.map(Node, self.get_subdirs())]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(path:{self.path},nodes:{self.nodes})"
    
    def get_subdirs(self) -> List[str]:
        subdirpaths: List[str] = list()
        for root, dirs, files in os.walk(self.path):
            subdirpaths.extend([os.path.join(root, dirname) for dirname in dirs])
        return subdirpaths
    
    def get_incomplete_logs(self) -> List[LogLeaflet]:
        incomplete_logs: List[LogLeaflet] = list()
        for node in self.nodes:
            incomplete_logs.extend(node.get_incomplete_logs())
        return incomplete_logs

    def get_unrun_coms(self) -> List[ComLeaflet]:
        unrun_coms: List[LogLeaflet] = list()
        for node in self.nodes:
            unrun_coms.extend(node.get_unrun_coms())
        return unrun_coms

    def get_coms_to_rerun(self) -> List[ComLeaflet]:
        coms_to_rerun: List[ComLeaflet] = list()
        for node in self.nodes:
            coms_to_rerun.extend(node.get_coms_to_rerun())
        return coms_to_rerun
