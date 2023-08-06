#   Imports
import xml.etree.ElementTree as ET

#   Class Imports
from mvr import GeneralSceneDescription, Layer, Fixture


def parse(mvr_path):
    layers_arr = []
    fixtures_arr = []

    if mvr_path:
        main_tree = ET.parse(mvr_path)  #   Parse XML File

        root = main_tree.getroot()  #   Get Root of XML File

        #   Root is an Array, [0] is UserData, [1] is Scene

        gsd = GeneralSceneDescription(root) #   Convert to Object

        layers = gsd.scene[0]

        for layer in layers:
            layers_arr.append(Layer(layer))

        for layer_obj in layers_arr:
            fixtures = layer_obj.child_list
            for fixture in fixtures:
                fixtures_arr.append(Fixture(fixture))

        mvr_file = {"gsd": gsd, "Layers": layers_arr, "Fixtures": fixtures_arr}
            
        return mvr_file