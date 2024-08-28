from typing import List
import glob

from leaflet import Leaflet
from comleaflet import ComLeaflet
from logleaflet import LogLeaflet

class Node:
    def __init__(self, dirpath: str):
        self.leaflets: List[Leaflet] = list()
        for filepath in glob.glob(f"{dirpath}/*"):
            if ".com" in filepath:
                self.leaflets.append(ComLeaflet(filepath))
            elif ".log" in filepath:
                self.leaflets.append(LogLeaflet(filepath))
            else:
                self.leaflets.append(Leaflet(filepath))
    
    def get_leaflets(self) -> List[Leaflet]:
        return self.leaflets
    
    def get_leaflets_bytype(self, desiredclass) -> List[Leaflet]:
        return [leaflet for leaflet in self.leaflets if isinstance(leaflet, desiredclass)]
    
    def get_incomplete_logs(self) -> List[str]:
        return [logleaflet.get_path() for logleaflet in self.get_leaflets_bytype(LogLeaflet) if not logleaflet.is_completed()]
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(leaflets:{self.leaflets})"