import os

class Leaflet:
    def __init__(self, path: str):
        self.path: str = path
        with open(self.path, 'r') as f:
            self.contents: List[str] = f.read().splitlines()
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(path:\"{self.path}\")"
    
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

    def get_contents(self) -> str:
        return self.contents

    def head(self, numlines: int) -> str:
        lines: List[str] = self.get_contents()
        if numlines < 1:
            raise ValueError(f"Parameter numlines must be a positive integer. Your value: {numlines}")
        return '\n'.join(lines[:numlines])

    def tail(self, numlines: int) -> str:
        lines: List[str] = self.get_contents()
        if numlines < 1:
            raise ValueError(f"Parameter numlines must be a positive integer. Your value: {numlines}")
        return '\n'.join(lines[-numlines:])
