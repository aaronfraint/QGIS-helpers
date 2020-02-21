"""
Summary of ``xyz.py``
-------------------------

Use the sources defined below to add entries under XYZ within the QGIS Browser.

Examples
--------

Within QGIS, open the Python command prompt and type:

    >>> import browser_helpers as bh
    >>> bh.add_xyz_connections()

"""

from qgis.PyQt.QtCore import QSettings
from qgis.utils import iface

# format:
# display name, authcfg, pw, referer, url, username, zmax, zmin

google_sources = [
    ["Google Maps","","","","https://mt1.google.com/vt/lyrs=m&x=%7Bx%7D&y=%7By%7D&z=%7Bz%7D","","19","0"],
    ["Google Satellite", "", "", "", "https://mt1.google.com/vt/lyrs=s&x=%7Bx%7D&y=%7By%7D&z=%7Bz%7D", "", "19", "0"],
    ["Google Terrain", "", "", "", "https://mt1.google.com/vt/lyrs=t&x=%7Bx%7D&y=%7By%7D&z=%7Bz%7D", "", "19", "0"],
    ["Google Terrain Hybrid", "", "", "", "https://mt1.google.com/vt/lyrs=p&x=%7Bx%7D&y=%7By%7D&z=%7Bz%7D", "", "19", "0"],
    ["Google Satellite Hybrid", "", "", "", "https://mt1.google.com/vt/lyrs=y&x=%7Bx%7D&y=%7By%7D&z=%7Bz%7D", "", "19", "0"],
]

stamen_sources = [
    ["Stamen Toner", "", "", "Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL", "http://tile.stamen.com/toner/%7Bz%7D/%7Bx%7D/%7By%7D.png", "", "20", "0"],
    ["Stamen Toner Light", "", "", "Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL", "http://tile.stamen.com/toner-lite/%7Bz%7D/%7Bx%7D/%7By%7D.png", "", "20", "0"],
    ["Stamen Watercolor", "", "", "Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL", "http://tile.stamen.com/watercolor/%7Bz%7D/%7Bx%7D/%7By%7D.jpg", "", "18", "0"],
    ["Stamen Terrain", "", "", "Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL", "http://tile.stamen.com/terrain/%7Bz%7D/%7Bx%7D/%7By%7D.png", "", "20", "0"],
]

esri_sources = [
    ["Esri Boundaries Places", "", "", "", "https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/%7Bz%7D/%7By%7D/%7Bx%7D", "", "20", "0"],
    ["Esri Gray (dark)", "", "", "", "http://services.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/%7Bz%7D/%7By%7D/%7Bx%7D", "", "16", "0"],
    ["Esri Gray (light)", "", "", "", "http://services.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/%7Bz%7D/%7By%7D/%7Bx%7D", "", "16", "0"],
    ["Esri National Geographic", "", "", "", "http://services.arcgisonline.com/ArcGIS/rest/services/NatGeo_World_Map/MapServer/tile/%7Bz%7D/%7By%7D/%7Bx%7D", "", "12", "0"],
    ["Esri Ocean", "", "", "", "https://services.arcgisonline.com/ArcGIS/rest/services/Ocean/World_Ocean_Base/MapServer/tile/%7Bz%7D/%7By%7D/%7Bx%7D", "", "10", "0"],
    ["Esri Satellite", "", "", "", "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/%7Bz%7D/%7By%7D/%7Bx%7D", "", "17", "0"],
    ["Esri Standard", "", "", "", "https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/%7Bz%7D/%7By%7D/%7Bx%7D", "", "17", "0"],
    ["Esri Terrain", "", "", "", "https://server.arcgisonline.com/ArcGIS/rest/services/World_Terrain_Base/MapServer/tile/%7Bz%7D/%7By%7D/%7Bx%7D", "", "13", "0"],
    ["Esri Transportation", "", "", "", "https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Transportation/MapServer/tile/%7Bz%7D/%7By%7D/%7Bx%7D", "", "20", "0"],
    ["Esri Topo World", "", "", "", "http://services.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/%7Bz%7D/%7By%7D/%7Bx%7D", "", "20", "0"],
]

osm_sources = [
    ["OpenStreetMap Standard", "", "", "OpenStreetMap contributors, CC-BY-SA", "http://tile.openstreetmap.org/%7Bz%7D/%7Bx%7D/%7By%7D.png", "", "19", "0"],
    ["OpenStreetMap H.O.T.", "", "", "OpenStreetMap contributors, CC-BY-SA", "http://tile.openstreetmap.fr/hot/%7Bz%7D/%7Bx%7D/%7By%7D.png", "", "19", "0"],
    ["OpenStreetMap Monochrome", "", "", "OpenStreetMap contributors, CC-BY-SA", "http://tiles.wmflabs.org/bw-mapnik/%7Bz%7D/%7Bx%7D/%7By%7D.png", "", "19", "0"],
]

SOURCES = google_sources + stamen_sources + esri_sources + osm_sources


def remove_xyz_connections():
    """ Remove all XYZ entries in the Browser """
    qs = QSettings()

    for k in sorted(qs.allKeys()):
        if "qgis/connections-xyz/" in k:
            qs.remove(k)

    iface.reloadConnections()


def add_xyz_connections(
        extra_sources: list = [],
        remove_existing: bool = True,
) -> None:
    """
    Add XYZ connection for all default and user-specified sources

    The format for custom sources is:
        - ``[display name, authcfg, pw, referer, url, username, zmax, zmin]``


    :param extra_sources: user-provided list to extend the stock choices
    :param remove_existing: if True, will clear out old connections before adding new ones
    """

    if remove_existing:
        remove_xyz_connections()

    sources = SOURCES + extra_sources

    # Add sources to browser
    for source in sources:
        connectionName = source[0]
        value_prefix = f"qgis/connections-xyz/{connectionName}"
        QSettings().setValue(f"{value_prefix}/authcfg", source[1])
        QSettings().setValue(f"{value_prefix}/password", source[2])
        QSettings().setValue(f"{value_prefix}/referer", source[3])
        QSettings().setValue(f"{value_prefix}/url", source[4])
        QSettings().setValue(f"{value_prefix}/username", source[5])
        QSettings().setValue(f"{value_prefix}/zmax", source[6])
        QSettings().setValue(f"{value_prefix}/zmin", source[7])

    iface.reloadConnections()
