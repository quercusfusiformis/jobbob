from leaflet import Leaflet

class ComLeaflet(Leaflet):
    def get_nprocshared(self) -> int:
        for line in self.head(5).splitlines():
            if "nprocshared" in line.lower():
                return int(line.split('=')[-1])
        return None

    def get_mem(self) -> str:
        for line in self.head(5).splitlines():
            if "mem" in line.lower():
                return line.split('=')[-1]
        return None
