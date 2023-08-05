# -*- coding: utf-8 -*-

# enpt_enmapboxapp, A QGIS EnMAPBox plugin providing a GUI for the EnMAP processing tools (EnPT)
#
# Copyright (C) 2018-2022 Daniel Scheffler (GFZ Potsdam, daniel.scheffler@gfz-potsdam.de)
#
# This software was developed within the context of the EnMAP project supported
# by the DLR Space Administration with funds of the German Federal Ministry of
# Economic Affairs and Energy (on the basis of a decision by the German Bundestag:
# 50 EE 1529) and contributions from DLR, GFZ and OHB System AG.
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

"""This module provides a QGIS EnMAPBox GUI for the EnMAP processing tools (EnPT)."""
import os
import traceback
from pkgutil import find_loader
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QMenu, QAction, QMessageBox
from enmapbox.gui.applications import EnMAPBoxApplication as _EnMAPBoxApplication
from qgis.core import QgsApplication, Qgis

from .version import __version__
from .enpt_algorithm import EnPTAlgorithm
from .enpt_external_algorithm import ExternalEnPTAlgorithm

VERSION = __version__
LICENSE = 'GNU GPL-3'
APP_DIR = os.path.dirname(__file__)
APP_NAME = 'EnPT EnMAPBox App'


class EnPTEnMAPBoxApp(_EnMAPBoxApplication):
    """The EnPT GUI class."""

    def __init__(self, enmapBox, parent=None):
        super(EnPTEnMAPBoxApp, self).__init__(enmapBox, parent=parent)

        self.name = APP_NAME
        self.version = VERSION
        self.licence = LICENSE
        self.enpt_is_external = not find_loader('enpt')
        self.ALG = EnPTAlgorithm if not self.enpt_is_external else ExternalEnPTAlgorithm

    def icon(self):
        """Return the QIcon of EnPTEnMAPBoxApp.

        :return: QIcon()
        """
        return QIcon(os.path.join(APP_DIR, 'icon.png'))

    def menu(self, appMenu):
        """Return a QMenu that will be added to the parent `appMenu`.

        :param appMenu:
        :return: QMenu
        """
        assert isinstance(appMenu, QMenu)
        """
        Specify menu, submenus and actions that become accessible from the EnMAP-Box GUI
        :return: the QMenu or QAction to be added to the "Applications" menu.
        """

        # this way you can add your QMenu/QAction to another menu entry, e.g. 'Tools'
        # appMenu = self.enmapbox.menu('Tools')

        menu_entry = 'EnPT (EnMAP Processing Tool)'
        _alphabetic_menu = False
        try:
            # alphabetic menu was implemented in EnMAP-Box around 3.10.1
            menu = self.utilsAddMenuInAlphabeticOrder(appMenu, menu_entry)
            _alphabetic_menu = True
        except AttributeError:
            menu = appMenu.addMenu(menu_entry)
        menu.setIcon(self.icon())

        # add a QAction that starts a process of your application.
        # In this case it will open your GUI.
        a = menu.addAction('About EnPT')
        a.triggered.connect(self.showAboutDialog)
        a = menu.addAction('Start EnPT GUI')
        assert isinstance(a, QAction)
        a.triggered.connect(self.startGUI)

        if not _alphabetic_menu:
            appMenu.addMenu(menu)

        return menu

    def showAboutDialog(self):
        QMessageBox.information(
            None, self.name,
            'EnPT (the EnMAP processing tool) is an automated pre-processing pipeline for the new EnMAP hyperspectral '
            'satellite data. It provides free and open-source features to transform EnMAP Level-1B data to Level-2A. '
            'The code has been developed at the German Research Centre for Geosciences Potsdam (GFZ) as an alternative '
            'to the processing chain of the EnMAP Ground Segment.\n'
            '\n'
            'Installed GUI version: {}'.format(self.version))

    def processingAlgorithms(self):
        """Return the QGIS Processing Framework GeoAlgorithms specified by your application.

        :return: [list-of-GeoAlgorithms]
        """
        return [self.ALG()]

    def startGUI(self):
        """Open the GUI."""
        try:
            from processing.gui.AlgorithmDialog import AlgorithmDialog

            alg = QgsApplication.processingRegistry().algorithmById('enmapbox:EnPTAlgorithm')
            assert isinstance(alg, self.ALG)
            dlg = AlgorithmDialog(alg.create(), in_place=False, parent=self.enmapbox.ui)
            dlg.show()

            return dlg

        except Exception as ex:
            msg = str(ex)
            msg += '\n' + str(traceback.format_exc())
            self.enmapbox.messageBar().pushMessage(APP_NAME, 'Error', msg, level=Qgis.Critical, duration=10)

            return None
