from leaflet import Leaflet
from comleaflet import ComLeaflet
from logleaflet import LogLeaflet
from node import Node

if __name__ == "__main__":
    pass
    # Leaflet
    leaflet = Leaflet("/home/breadbear/proj/jobbob/data/AFOHIM/Frag_1.log")
    # print(leaflet)
    # print(leaflet.get_path())
    # print(leaflet.get_path_basename())
    # print(leaflet.get_path_dirname())
    # print(leaflet.get_path_noext())
    # print(leaflet.get_path_ext())
    # print(leaflet.cat())
    # print(leaflet.head(10))
    # print(leaflet.tail(10))

    ## LogLeaflet
    logleaflet = LogLeaflet("/home/breadbear/proj/jobbob/data/AFOHIM/Frag_1.log")
    # print(logleaflet)
    # print(logleaflet.is_completed())

    ## ComLeaflet
    comleaflet = ComLeaflet("/home/breadbear/proj/jobbob/data/AFOHIM/Frag_1.com")
    # print(comleaflet)
    # print(comleaflet.get_nprocshared())
    # print(comleaflet.get_mem())

    ## Node
    node = Node("/home/breadbear/proj/jobbob/data/AFOHIM")
    print(node)
    print(node.get_leaflets())
    print(node.get_leaflets_bytype(ComLeaflet))
    print(node.get_incomplete_logs())
