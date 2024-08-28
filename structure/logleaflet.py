from leaflet import Leaflet

class LogLeaflet(Leaflet):
    def is_completed(self) -> bool:
        for line in self.tail(5).splitlines():
            if "Normal termination of Gaussian" in line:
                return True
        return False
