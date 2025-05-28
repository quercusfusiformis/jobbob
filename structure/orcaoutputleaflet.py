from leaflet import Leaflet

NUM_LINES_IN_COMPLETION_SEARCH: int = 5
NUM_LINES_IN_ERROR_SEARCH: int = 10

class OrcaOutputLeaflet(Leaflet):
    def is_completed(self) -> bool:
        for line in self.tail(NUM_LINES_IN_COMPLETION_SEARCH).splitlines():
            if "****ORCA TERMINATED NORMALLY****" in line:
                return True
        return False
    
    def has_impossible_mult_electr(self) -> bool:
        for line in self.tail(NUM_LINES_IN_ERROR_SEARCH).splitlines():
            if all(val in line for val in ["multiplicity", "number of electrons", "-> impossible"]):
                return True
        return False
