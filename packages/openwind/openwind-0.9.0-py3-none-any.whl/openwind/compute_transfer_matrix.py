#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2019-2021, INRIA
#
# This file is part of Openwind.
#
# Openwind is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Openwind is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Openwind.  If not, see <https://www.gnu.org/licenses/>.
#
# For more informations about authors, see the CONTRIBUTORS file

import warnings
import numpy as np
from openwind.technical import InstrumentGeometry, Player
from openwind.continuous import InstrumentPhysics
from openwind.frequential import FrequentialSolver



def ComputeTransferMatrix(geom, freq, temperature, losses=True, **discr_param):
    """
    Computes the transfer matrix for a given geometry and for a frequency range

    Parameters
    ----------
    geom : string or list
        path to instrument geometry file ; or list describing the geometry.
    freq : ndarray or list
        frequency range.
    temperature : float
        The temperature in Celcius degree.
    losses : Boolean, optional
        Defines if losses are taken into account in computation.
        The default is True.
    **discr_param : keyword arguments
        Discretization parameters. See: :py:class:`Mesh <openwind.discretization.mesh.Mesh>`

    Returns
    -------
    a, b, c, d : 4 ndarray with same length as freq
        The four coefficients of the transfer matrix

    """
    instr_geom = InstrumentGeometry(geom)
    player = Player()

    closed_instr = InstrumentPhysics(instr_geom,
                                     temperature=temperature,
                                     player=player,
                                     losses=losses,
                                     radiation_category='closed')

    open_instr = InstrumentPhysics(instr_geom,
                                   temperature=temperature,
                                   player=player,
                                   losses=losses,
                                   radiation_category='perfectly_open')

    closed_model = FrequentialSolver(closed_instr, freq, **discr_param)

    open_model = FrequentialSolver(open_instr, freq, **discr_param)

    closed_model.solve(interp=True)
    open_model.solve(interp=True)

    # closed end : u2 = 0 ; a = p1/p2 ; c = u1 / p2
    # open end :   p2 = 0 ; b = p2/u2 ; d = u1 / u2
    p_closed = np.array(closed_model.pressure)
    u_closed = np.array(closed_model.flow)
    p_open = np.array(open_model.pressure)
    u_open = np.array(open_model.flow)
    a = p_closed[:, 0]/p_closed[:, -1]
    b = p_open[:, 0]/u_open[:, -1]
    c = u_closed[:, 0]/p_closed[:, -1]
    d = u_open[:, 0]/u_open[:, -1]

    if not np.all(np.isclose(a*d - c*b, 1)):
        f_min = np.min(np.array(freq)[~(np.isclose(a*d - c*b, 1))])
        f_max = np.max(np.array(freq)[~(np.isclose(a*d - c*b, 1))])
        warnings.warn('determinant of transfer matrix is not close to 1 ' +
                       'for frequencies in [{:.2f}, {:.2f}] Hz.'.format(f_min, f_max))

    return a, b, c, d
