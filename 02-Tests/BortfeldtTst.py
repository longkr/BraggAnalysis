#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "Bortfeldt" class ... initialisation and get methods
===========================

  Bortfeldt.py -- set "relative" path to code

"""

import os

import Bortfeldt as Bortfeldt


##! Start:
print("========  Bortfeldt: tests start  ========")

##! Test singleton class feature:
BortfeldtTest = 1
print()
print("BortfeldtTest:", BortfeldtTest, " check if class is a singleton.")
BraggPATH = os.getenv('BraggPATH')
print(BraggPATH)
filename  = os.path.join(BraggPATH, \
                         '11-BraggParameters/BraggParameters.csv')
iBortfeldt  = Bortfeldt.Bortfeldt(filename)
iBortfeldt1 = Bortfeldt.Bortfeldt(filename)
print("    iBortfeldt singleton test -- OK if 0:", id(iBortfeldt)-id(iBortfeldt1))
if iBortfeldt != iBortfeldt1:
    raise Exception("Bortfeldt is not a singleton class!")


##! Check built-in methods:
BortfeldtTest +- 1
print()
print("BortfeldtTest:", BortfeldtTest, " check built-in methods.")
print("    ----> __repr__:")
print(repr(iBortfeldt))
print("    ----> __str__:")
print(iBortfeldt)


##! Check calculation of theta0:
BortfeldtTest += 1
print()
print("BortfeldtTest:", BortfeldtTest, " check calculation of Bortfeldt.")
T = 100.
Ans = iBortfeldt.getBortfeldt(T)
print("     ---> T =", T, " MeV: Bortfeldt =", Ans)


##! Complete:
print()
print("========  Bortfeldt: tests complete  ========")
