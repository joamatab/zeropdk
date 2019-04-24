from klayout.db import LayerInfo


class Tech:
    layers = None

    def __init__(self):
        if self.layers is None:
            self.layers = dict()

    def create_layer(self, layer_name, layer_def):
        self.layers[layer_name] = layer_def

    @classmethod
    def load_from_xml(cls, lyp_filename):
        with open(lyp_filename, 'r') as file:
            layer_dict = xml_to_dict(file.read())['layer-properties']['properties']

        layer_map = {}

        for k in layer_dict:
            layerInfo = k['source'].split('@')[0]
            if 'group-members' in k:
                # encoutered a layer group, look inside:
                j = k['group-members']
                if 'name' in j:
                    layerInfo_j = j['source'].split('@')[0]
                    layer_map[j['name']] = layerInfo_j
                else:
                    for j in k['group-members']:
                        layerInfo_j = j['source'].split('@')[0]
                        layer_map[j['name']] = layerInfo_j
                if k['source'] != '*/*@*':
                    layer_map[k['name']] = layerInfo
            else:
                layer_map[k['name']] = layerInfo

        obj = cls()
        obj.layers.update(layer_map)
        return obj

# XML functions


def etree_to_dict(t):
    '''XML to Dict parser
    from: https://stackoverflow.com/questions/2148119/how-to-convert-an-xml-string-to-a-dictionary-in-python/10077069
    '''
    from collections import defaultdict
    d = {t.tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(etree_to_dict, children):
            for k, v in dc.items():
                dd[k].append(v)
        d = {t.tag: {k: v[0] if len(v) == 1 else v for k, v in dd.items()}}
    if t.attrib:
        d[t.tag].update(('@' + k, v) for k, v in t.attrib.items())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
                d[t.tag]['#text'] = text
        else:
            d[t.tag] = text
    return d


def xml_to_dict(t):
    from xml.etree import ElementTree as ET
    try:
        e = ET.XML(t)
    except ET.ParseError:
        raise
    except Exception:
        raise UserWarning("Error in the XML file.")
    return etree_to_dict(e)
