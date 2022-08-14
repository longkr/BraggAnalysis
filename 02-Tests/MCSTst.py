#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "MCS" class ... initialisation and get methods
===========================

  MCS.py -- set "relative" path to code

"""

import os

import MCS as MCS


##! Start:
print("========  MCS: tests start  ========")

##! Test singleton class feature:
MCSTest = 1
print()
print("MCSTest:", MCSTest, " check if class is a singleton.")
BraggPATH = os.getenv('BraggPATH')
print(BraggPATH)
filename  = os.path.join(BraggPATH, \
                         '11-MCS-parameters/MCS-parameters.csv')
iMCS  = MCS.MCS(filename)
iMCS1 = MCS.MCS(filename)
print("    iMCS singleton test -- OK if 0:", id(iMCS)-id(iMCS1))
if iMCS != iMCS1:
    raise Exception("MCS is not a singleton class!")


##! Check built-in methods:
MCSTest +- 1
print()
print("MCSTest:", MCSTest, " check built-in methods.")
print("    ----> __repr__:")
print(repr(iMCS))
print("    ----> __str__:")
print(iMCS)


##! Check calculation of theta0:
MCSTest += 1
print("MCSTest:", MCSTest, " check calculation of theta0.")
x = 10.
K = 100.
Theta0 = iMCS.getTheta0(x, K)
print("     ---> x =", x, " cm; K =", K, " MeV: theta0 =", Theta0)


##! Check calculation of Yplane:
MCSTest += 1
print("MCSTest:", MCSTest, " check calculation of Yplane.")
x = 10.
K = 100.
Yplane = iMCS.getYplane(x, K)
print("     ---> x =", x, " cm; K =", K, " MeV: Yplane =", Yplane)


##! Complete:
print()
print("========  MCS: tests complete  ========")
