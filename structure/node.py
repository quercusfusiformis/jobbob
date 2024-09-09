from typing import List
import os
import glob
from concurrent.futures import ProcessPoolExecutor

from leaflet import Leaflet
from gaussianinputleaflet import GaussianInputLeaflet
from gaussianoutputleaflet import GaussianOutputLeaflet
import num_generating_processes as ngp

def create_respective_leaflet(filepath: str) -> Leaflet:
    if ".com" in filepath or ".gjf" in filepath:
        return GaussianInputLeaflet(filepath)
    elif ".log" in filepath:
        return GaussianOutputLeaflet(filepath)
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
    
    def get_incomplete_gaussian_outputs(self) -> List[GaussianOutputLeaflet]:
        return [outputleaflet for outputleaflet in self.get_leaflets_bytype(GaussianOutputLeaflet) if not outputleaflet.is_completed()]
    
    def has_incomplete_gaussian_outputs(self) -> bool:
        return len(self.get_incomplete_gaussian_outputs()) > 0
    
    def get_unrun_gaussian_inputs(self) -> List[GaussianInputLeaflet]:
        output_basenames: List[str] = [outputleaflet.get_path_noext() for outputleaflet in self.get_leaflets_bytype(GaussianOutputLeaflet)]
        return [inputleaflet for inputleaflet in self.get_leaflets_bytype(GaussianInputLeaflet) if inputleaflet.get_path_noext() not in output_basenames]
    
    def get_gaussian_inputs_to_rerun(self) -> List[GaussianInputLeaflet]:
        inputs_to_rerun: List[GaussianInputLeaflet] = list()
        failed_output_basenames: List[str] = [outputleaflet.get_path_noext() for outputleaflet in self.get_incomplete_gaussian_outputs()]
        inputs_to_rerun.extend([inputleaflet for inputleaflet in self.get_leaflets_bytype(GaussianInputLeaflet) if inputleaflet.get_path_noext() in failed_output_basenames])
        inputs_to_rerun.extend(self.get_unrun_gaussian_inputs())
        return inputs_to_rerun
