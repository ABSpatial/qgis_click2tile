# -*- coding: utf-8 -*-
import math
import os

import mercantile
from PyQt5.QtCore import QObject, Qt, QLocale
from qgis.PyQt.QtWidgets import QAction
from qgis.gui import QgsMapToolEmitPoint

from .click_to_tile_dockwidget import ClickToTileDockWidget


def scale_to_zoom(scale):
    zoom = math.log2(591657550.5 / scale)
    return round(zoom)


class ClickToTile(QObject):

    def __init__(self, iface):
        QObject.__init__(self)
        self.iface = iface
        self.canvas = iface.mapCanvas()
        self.plugin_dir = os.path.dirname(__file__)
        self.locale = QLocale()

        # Initialize the map tool
        self.map_tool = QgsMapToolEmitPoint(self.canvas)
        self.map_tool.canvasClicked.connect(self.handle_map_click)

        # Initialize the dock widget
        self.dock_widget = ClickToTileDockWidget()
        self.iface.addDockWidget(Qt.LeftDockWidgetArea, self.dock_widget)

    def initGui(self):
        self.action = QAction("Click To Tile", self.iface.mainWindow())
        self.iface.addPluginToMenu("&ClickToTile", self.action)
        self.iface.addToolBarIcon(self.action)
        self.action.triggered.connect(self.toggle_map_tool)

    def unload(self):
        self.canvas.unsetMapTool(self.map_tool)
        self.iface.removePluginMenu("&ClickToTile", self.action)
        self.iface.removeToolBarIcon(self.action)
        self.iface.removeDockWidget(self.dock_widget)

    def toggle_map_tool(self):
        self.canvas.setMapTool(self.map_tool)

    def handle_map_click(self, point):
        x = point.x()
        y = point.y()
        self.dock_widget.update_coordinates(x, y, self.get_tile_coords(point))

    def get_tile_coords(self, point):
        # Assuming 'point' is a QgsPointXY object
        lon, lat = point.x(), point.y()
        zoom = scale_to_zoom(self.canvas.scale())
        tile = mercantile.tile(lon, lat, zoom)
        return tile.z, tile.x, tile.y
