from leaflet import Leaflet

NUM_LINES_IN_HEADER_SEARCH: int = 5

class ComLeaflet(Leaflet):
    def get_nprocshared(self) -> int:
        for line in self.head(NUM_LINES_IN_HEADER_SEARCH).splitlines():
            if "nprocshared" in line.lower():
                return int(line.split('=')[-1])
        return None

    def get_mem(self) -> str:
        for line in self.head(NUM_LINES_IN_HEADER_SEARCH).splitlines():
            if "mem" in line.lower():
                return line.split('=')[-1]
        return None
