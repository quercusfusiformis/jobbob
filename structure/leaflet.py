import os

class Leaflet:
    def __init__(self, path: str):
        self.path: str = path
    
    def get_path(self) -> str:
        return self.path
    
    def get_path_basename(self) -> str:
        return os.path.basename(self.path)
    
    def get_path_dirname(self) -> str:
        return os.path.dirname(self.path)
    
    def get_path_noext(self) -> str:
        return '.'.join((self.path).split('.')[:-1])
    
    def get_path_ext(self) -> str:
        return (self.path).split('.')[-1]

    def cat(self) -> str:
        with open(self.path, 'r') as f:
            readfile: List[str] = f.read()
        return readfile

    def head(self, numlines: int) -> str:
        lines: List[str] = self.cat().splitlines()
        if numlines < 1:
            raise ValueError(f"Parameter numlines must be a positive integer. Your value: {numlines}")
        return '\n'.join(lines[:numlines])

    def tail(self, numlines: int) -> str:
        lines: List[str] = self.cat().splitlines()
        if numlines < 1:
            raise ValueError(f"Parameter numlines must be a positive integer. Your value: {numlines}")
        return '\n'.join(lines[-numlines:])
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(path:\"{self.path}\")"
