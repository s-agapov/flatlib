"""
    This file is part of flatlib - (C) FlatAngle
    Author: João Ventura (flatangleweb@gmail.com)
    
    
    This module provides useful functions for computing 
    Arabic Parts.
  
"""

from flatlib import const
from flatlib.object import GenericObject
from flatlib.dignities import essential

# Define arabic parts
LOT_OF_FORTUNE = const.PARS_FORTUNA
LOT_OF_SPIRIT = 'Lot of Spirit'
LOT_OF_EROS = 'Lot of Eros'
LOT_OF_NECESSITY = 'Lot of Necessity'
LOT_OF_COURAGE = 'Lot of Courage'
LOT_OF_VICTORY = 'Lot of Victory'
LOT_OF_NEMESIS = 'Lot of Nemesis'
LOT_OF_DESIRE = 'Lot of Desire'
LOT_OF_AVERSION = 'Lot of Aversion'

# Define Diurnal and Nocturnal formulas as
# "Distance from A to B counterclockwise around zodiac + C".
# Brennan. Helenistic Astrology.16 on Lots. Calculation and Conceptualization
# Note that '$R' stands for the Ruler of something
FORMULAS = {}


### Heremetic Lots

FORMULAS[LOT_OF_FORTUNE] = [
    [const.SUN, const.MOON, const.ASC],  # Diurnal
    [const.MOON, const.SUN, const.ASC]  # Nocturnal
]

FORMULAS[LOT_OF_SPIRIT] = [
    [const.MOON, const.SUN, const.ASC],
    [const.SUN, const.MOON, const.ASC]
]

FORMULAS[LOT_OF_EROS] = [
    [LOT_OF_SPIRIT, const.VENUS, const.ASC],
    [const.VENUS, LOT_OF_SPIRIT, const.ASC]
]

FORMULAS[LOT_OF_NECESSITY] = [
    [const.MERCURY, LOT_OF_FORTUNE, const.ASC],
    [LOT_OF_FORTUNE, const.MERCURY, const.ASC]
]

FORMULAS[LOT_OF_COURAGE] = [
    [const.MARS, LOT_OF_FORTUNE, const.ASC],
    [LOT_OF_FORTUNE, const.MARS, const.ASC]
]

FORMULAS[LOT_OF_VICTORY] = [
    [LOT_OF_SPIRIT, const.JUPITER, const.ASC],
    [const.JUPITER, LOT_OF_SPIRIT, const.ASC]
]

FORMULAS[LOT_OF_NEMESIS] = [
    [const.SATURN, LOT_OF_FORTUNE, const.ASC],
    [LOT_OF_FORTUNE, const.SATURN, const.ASC]
]

# Valens 4, 35:13 epithumia
FORMULAS[LOT_OF_DESIRE] = [
    [LOT_OF_FORTUNE, LOT_OF_SPIRIT, const.ASC],
    [LOT_OF_SPIRIT, LOT_OF_FORTUNE, const.ASC]
]

#Valens 4,25:16. 2,16:1 echthron
FORMULAS[LOT_OF_AVERSION] = [
    [LOT_OF_SPIRIT, LOT_OF_FORTUNE, const.ASC],
    [LOT_OF_FORTUNE, LOT_OF_SPIRIT, const.ASC],
]


# === Functions === #

def objLon(ID, chart):
    """ Returns the longitude of an object. """
    if ID.startswith('$R'):
        # Return Ruler
        ID = ID[2:]
        obj = chart.get(ID)
        rulerID = essential.ruler(obj.sign)
        ruler = chart.getObject(rulerID)
        return ruler.lon
    elif ID.startswith('Lot'):
        # Return a Lot
        return partLon(ID, chart)
    else:
        # Return an object
        obj = chart.get(ID)
        return obj.lon


def partLon(ID, chart):
    """ Returns the longitude of an arabic part. """
    # Get diurnal or nocturnal formula
    abc = FORMULAS[ID][0] if chart.isDiurnal() else FORMULAS[ID][1]
    a = objLon(abc[0], chart)
    b = objLon(abc[1], chart)
    c = objLon(abc[2], chart)
    return c + b - a


def getLot(ID, chart):
    """ Returns an Lot. """
    obj = GenericObject()
    obj.id = ID
    obj.type = const.OBJ_ARABIC_PART
    obj.relocate(partLon(ID, chart))
    return obj
