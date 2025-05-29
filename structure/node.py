from pathlib import Path

from leaflet import Leaflet
from gaussianinputleaflet import GaussianInputLeaflet
from gaussianoutputleaflet import GaussianOutputLeaflet
from orcainputleaflet import OrcaInputLeaflet
from orcaoutputleaflet import OrcaOutputLeaflet

def create_respective_leaflet(path: Path) -> Leaflet:
    if path.suffix == ".com" or path.suffix == ".gjf":
        return GaussianInputLeaflet(path=path)
    elif path.suffix == ".log":
        return GaussianOutputLeaflet(path=path)
    elif path.suffix == ".inp":
        return OrcaInputLeaflet(path=path)
    elif path.suffix == ".out" and "slurm" not in path.stem.lower():
        return OrcaOutputLeaflet(path=path)
    else:
        return Leaflet(path=path)

class Node:
    def __init__(self, pathstr: str):
        self.path: Path = Path(pathstr)
        self.leaflets: tuple[Leaflet] = tuple(create_respective_leaflet(path=filepath) for filepath in self.get_subfiles())

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(path:{self.path},leaflets:{self.leaflets})"
    
    def get_subfiles(self) -> tuple[Path]:
        subfile_paths: list[Path] = list()
        for path, dirnames, filenames in self.path.walk():
            subfile_paths.extend(tuple(path.joinpath(filename) for filename in filenames))
        return subfile_paths

    def get_leaflets(self) -> tuple[Leaflet]:
        return self.leaflets
    
    def get_leaflets_bytype(self, desiredclass) -> tuple[Leaflet]:
        return tuple(leaflet for leaflet in self.leaflets if isinstance(leaflet, desiredclass))
    
    def get_incomplete_gaussian_outputs(self) -> tuple[GaussianOutputLeaflet]:
        return tuple(outputleaflet for outputleaflet in self.get_leaflets_bytype(GaussianOutputLeaflet) if not outputleaflet.is_completed())
    
    def has_incomplete_gaussian_outputs(self) -> bool:
        return len(self.get_incomplete_gaussian_outputs()) > 0
    
    def get_unrun_gaussian_inputs(self) -> tuple[GaussianInputLeaflet]:
        output_stems: tuple[str] = tuple(outputleaflet.path.stem for outputleaflet in self.get_leaflets_bytype(GaussianOutputLeaflet))
        return tuple(inputleaflet for inputleaflet in self.get_leaflets_bytype(GaussianInputLeaflet) if inputleaflet.path.stem not in output_stems)
    