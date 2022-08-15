#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Find trends in MCS, dEdx, and dose:
===================================

"""

import os
import math as mth

import MCS  as mcs
import dEdx as dedx

BraggPATH = os.getenv('BraggPATH')
filename  = os.path.join(BraggPATH, \
                         '11-BraggParameters/BraggParameters.csv')

iMCS  = mcs.MCS(filename)
idEdx = dedx.dEdx(filename)

##! Start:
print("========  Trend evaluation start  ========")

##! Trends as function of kinetic energy, T:

T0 = 200.                #.. MeV
x  =   0.05              #.. cm
dx =   0.1               #.. cm
r0 =   0.1               #.. cm

T  = T0

while T > 0.:

    #..  Calculate yplane, effective area, effective volume
    yPlane = iMCS.getYplane(x, T)
    dE     = idEdx.getdEdx(T) * dx

    E      = idEdx.getProjectileMass() + T
    P      = mth.sqrt(E**2 - idEdx.getProjectileMass()*2)
    gamma  = E/P
    beta   = mth.sqrt(gamma**2 - 1.) / gamma
    
    #..  Output:
    print(x, T, E, P, gamma, beta, yPlane, dE)

    #..  Increment x and energy
    x += dx
    T -= dE
    
##! Complete:
print()
print("========  Trend evaluation complete  ========")
