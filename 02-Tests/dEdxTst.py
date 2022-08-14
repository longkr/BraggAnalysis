#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "dEdx" class ... initialisation and get methods
===========================

  dEdx.py -- set "relative" path to code

"""

import os

import dEdx as dEdx


##! Start:
print("========  dEdx: tests start  ========")

##! Test singleton class feature:
dEdxTest = 1
print()
print("dEdxTest:", dEdxTest, " check if class is a singleton.")
BraggPATH = os.getenv('BraggPATH')
print(BraggPATH)
filename  = os.path.join(BraggPATH, \
                         '11-BraggParameters/BraggParameters.csv')
idEdx  = dEdx.dEdx(filename)
idEdx1 = dEdx.dEdx(filename)
print("    idEdx singleton test -- OK if 0:", id(idEdx)-id(idEdx1))
if idEdx != idEdx1:
    raise Exception("dEdx is not a singleton class!")


##! Check built-in methods:
dEdxTest +- 1
print()
print("dEdxTest:", dEdxTest, " check built-in methods.")
print("    ----> __repr__:")
print(repr(idEdx))
print("    ----> __str__:")
print(idEdx)


##! Check calculation of theta0:
dEdxTest += 1
print()
print("dEdxTest:", dEdxTest, " check calculation of dEdx.")
T = 100.
Ans = idEdx.getdEdx(T)
print("     ---> T =", T, " MeV: dEdx =", Ans)


##! Complete:
print()
print("========  dEdx: tests complete  ========")
