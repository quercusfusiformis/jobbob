from leaflet import Leaflet

NUM_LINES_IN_HEADER_SEARCH: int = 15

class OrcaInputLeaflet(Leaflet):
    def get_nprocs(self) -> int:
        for line in self.head(NUM_LINES_IN_HEADER_SEARCH).splitlines():
            if "pal" in line.lower():
                return int(line.lower().split("pal")[-1].split()[0])
            elif "nprocs" in line.lower():
                return int(line.split()[-1])
        return None

    def get_maxcore(self) -> str:
        for line in self.head(NUM_LINES_IN_HEADER_SEARCH).splitlines():
            if "maxcore" in line.lower():
                return line.split()[-1]
        return None
