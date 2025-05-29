from pathlib import Path

class Leaflet:
    def __init__(self, path: Path):
        self.path: Path = path
        with open(self.path, 'r', encoding="utf-8") as f:
            self.contents: list[str] = f.read().splitlines()
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(path:\"{self.path}\")"
    
    def head(self, numlines: int) -> str:
        lines: list[str] = self.contents
        if numlines < 1:
            raise ValueError(f"Parameter numlines must be a positive integer. Your value: {numlines}")
        return '\n'.join(lines[:numlines])

    def tail(self, numlines: int) -> str:
        lines: list[str] = self.contents
        if numlines < 1:
            raise ValueError(f"Parameter numlines must be a positive integer. Your value: {numlines}")
        return '\n'.join(lines[-numlines:])
