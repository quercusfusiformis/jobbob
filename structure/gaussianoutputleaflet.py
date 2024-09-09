from leaflet import Leaflet

NUM_LINES_IN_COMPLETION_SEARCH: int = 5
NUM_LINES_IN_ERROR_SEARCH: int = 10

class GaussianOutputLeaflet(Leaflet):
    def is_completed(self) -> bool:
        for line in self.tail(NUM_LINES_IN_COMPLETION_SEARCH).splitlines():
            if "Normal termination of Gaussian" in line:
                return True
        return False
    
    def has_impossible_mult_electr(self) -> bool:
        for line in self.tail(NUM_LINES_IN_ERROR_SEARCH).splitlines():
            if all(val in line for val in ["The combination of multiplicity", "electrons is impossible"]):
                return True
        return False
