from typing import List
import os
import glob
from concurrent.futures import ProcessPoolExecutor

from leaflet import Leaflet
from comleaflet import ComLeaflet
from logleaflet import LogLeaflet
import num_generating_processes as ngp

def create_respective_leaflet(filepath: str) -> Leaflet:
    if ".com" in filepath:
        return ComLeaflet(filepath)
    elif ".log" in filepath:
        return LogLeaflet(filepath)
    else:
        return Leaflet(filepath)

class Node:
    def __init__(self, dirpath: str):
        self.path: str = dirpath
        with ProcessPoolExecutor(ngp.LEAFLET_GENERATING_PROCESSES) as p:
            self.leaflets: List[Leaflet] = [leaflet for leaflet in p.map(create_respective_leaflet, self.get_subfiles())]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(path:{self.path},leaflets:{self.leaflets})"
    
    def get_subfiles(self) -> List[str]:
        subfilepaths: List[str] = list()
        for root, dirs, files in os.walk(self.path):
            subfilepaths.extend([os.path.join(root, filename) for filename in files])
        return subfilepaths

    def get_leaflets(self) -> List[Leaflet]:
        return self.leaflets
    
    def get_leaflets_bytype(self, desiredclass) -> List[Leaflet]:
        return [leaflet for leaflet in self.leaflets if isinstance(leaflet, desiredclass)]
    
    def get_incomplete_logs(self) -> List[LogLeaflet]:
        return [logleaflet for logleaflet in self.get_leaflets_bytype(LogLeaflet) if not logleaflet.is_completed()]
    
    def has_incomplete_logs(self) -> bool:
        return len(self.get_incomplete_logs()) > 0
    
    def get_unrun_coms(self) -> List[ComLeaflet]:
        logbasenames: List[str] = [logleaflet.get_path_noext() for logleaflet in self.get_leaflets_bytype(LogLeaflet)]
        combasenames: List[str] = [comleaflet.get_path_noext() for comleaflet in self.get_leaflets_bytype(ComLeaflet)]
        return [ComLeaflet(f"{combasename}.com") for combasename in combasenames if combasename not in logbasenames]
    
    def get_coms_to_rerun(self) -> List[ComLeaflet]:
        coms_to_rerun: List[ComLeaflet] = list()
        coms_to_rerun.extend([ComLeaflet(f"{logleaflet.get_path_noext()}.com") for logleaflet in self.get_incomplete_logs()])
        coms_to_rerun.extend(self.get_unrun_coms())
        return coms_to_rerun
