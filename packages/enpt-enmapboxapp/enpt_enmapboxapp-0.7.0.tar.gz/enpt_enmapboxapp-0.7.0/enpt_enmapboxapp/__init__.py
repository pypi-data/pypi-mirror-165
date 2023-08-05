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

"""Top-level package for enpt_enmapboxapp."""

from .version import __version__, __versionalias__   # noqa (E402 + F401)
from .enpt_algorithm import EnPTAlgorithm
from .enpt_external_algorithm import ExternalEnPTAlgorithm
from .enpt_enmapboxapp import EnPTEnMAPBoxApp

__author__ = """Daniel Scheffler"""
__email__ = 'danschef@gfz-potsdam.de'
__all__ = ['__version__',
           '__versionalias__',
           '__author__',
           '__email__',
           'EnPTAlgorithm',
           'ExternalEnPTAlgorithm',
           'EnPTEnMAPBoxApp'
           ]
