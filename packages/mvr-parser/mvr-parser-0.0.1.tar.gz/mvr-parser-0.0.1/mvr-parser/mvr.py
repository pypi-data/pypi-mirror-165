#   Imports
import math


#   Classes
class GeneralSceneDescription:
    def __init__(self, root):
        self.ver_major = root.attrib["verMajor"]
        self.ver_minor = root.attrib["verMinor"]
        self.user_data = root[0]
        self.scene = root[1]

class Layer:
    def __init__(self, layer):
        self.name = layer.attrib["name"]
        self.uuid = layer.attrib["uuid"]
        self.child_list = layer[0]

class Fixture:
    def __init__(self, fixture):
        self.matrix = fixture[0].text
        self.layer_class = fixture[1].text
        self.gdtf_spec = fixture[2].text
        self.manufacture = self.gdtf_spec.split('@', 1)[0]
        self.type = self.gdtf_spec.split('@', 1)[1]
        self.mode = fixture[3].text
        self.name = fixture.attrib["name"]
        self.uuid = fixture.attrib["uuid"]
        self.absolute_address = int(fixture[4][0].text)
        if int(fixture[4][0].text) > 512:
            self.universe = math.floor(int(fixture[4][0].text) / 512)
            self.address = int(fixture[4][0].text) - (512 * self.universe)
        else:
            self.universe = 1
            self.address = int(fixture[4][0].text)
        self.fixture_id = fixture[5].text

