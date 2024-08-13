# -*- coding: utf-8 -*-
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QDockWidget

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'click_to_tile_dockwidget_base.ui'))

class ClickToTileDockWidget(QDockWidget, FORM_CLASS):
    def __init__(self, parent=None):
        super(ClickToTileDockWidget, self).__init__(parent)
        self.setupUi(self)

    def update_coordinates(self, x, y, tile):
        self.x_coord.setText(str(x))
        self.y_coord.setText(str(y))
        print(str(tile))
        self.tile.setText(str(tile))
