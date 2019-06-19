def insert_shape(cell, layer, shape):
    if layer is not None:
        cell.shapes(layer).insert(shape)


import klayout.db as kdb


def layout_pgtext(cell, layer, x, y, text, mag, inv=False, angle=0):
    layout = kdb.Layout()
    lylayer = layout.layer(layer)
    pcell = layout.create_cell(
        "TEXT", "Basic", {"text": text, "layer": layer, "mag": mag, "inverse": inv}
    )
    pcell.transform_into(kdb.DCplxTrans(1, angle, False, x, y))
    lylayer_new = cell.layout().layer(layer)
    cell.shapes(lylayer_new).insert(pcell.shapes(lylayer))


from .polygons import *
from .waveguides import *
from .routing import *
