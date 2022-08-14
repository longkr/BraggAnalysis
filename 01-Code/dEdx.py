#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class dEdx:
===========

  Calculates the dEdx effect for a variety of situations.  Use singleton
  class so that instance attributes can be used to set the parameters.


  Class attributes:
  -----------------
  __instance : Set on creation of first (and only) instance.
  __Debug    : boolean ... debug flag      

  Instance attributes:
  --------------------
   __filename  = Filename from which parameters have been read.  If None
                 then default values are used.
   _dEdxParams  = Pandas data frame instance containing parameters
   _IssueDate  = date.today(); i.e. date when code is run and resuts are
                 generated 
    

  Methods:
  --------
  Built-in methods __new__, __repr__ and __str__.
      __new__ : Creates singleton class and prints version, PDG
                reference, and values of constants used.
      __repr__: One liner with call.
      __str__ : Dump of constants


  Get/set methods:   <-------- believed to be "self documenting"!

  Print methods:



  
Created on Thu 13Aug22, Version history:
----------------------------------------
 1.0: 13Aug22: First implementation

@author: kennethlong
"""

import os
import math   as     mth
import pandas as     pnds
from datetime import date

class dEdx(object):
    __instance = None
    __Debug    = True

#--------  "Built-in methods":
    def __new__(cls, _filename=None):

        if cls.__instance is None:
            cls.__instance = super(dEdx, cls).__new__(cls)
        
            if _filename == None:
                if  dEdx.__Debug:
                    print(" dEdx: no filename provided, take defaults.")
            elif not os.path.isfile(_filename):
                print(" dEdx: file ", _filename, " does not exist.", \
                      " Raising exception")
                raise NonExistantFile('CSV file' + \
                                      _filename + \
                                      ' does not exist; execution termimated.')

            #.. Set defaults:
            cls._filename  = None
            cls._IssueDate = date.today()
            cls._dEdxParams = None

            #.. Parse control file:
            if _filename != None:
                cls._cntrlParams = cls.getdEdxs(_filename)
                if cls.__Debug:
                    print(" dEdx: parameters: \n", \
                          cls._cntrlParams)
                    cls._K, cls._KUnit, cls._Z, cls._A, cls._z, \
                    cls._Eta1, cls._Eta1Unit, \
                    cls._Mp, cls._MpUnit, \
                    = cls.parsedEdx()
        
        return cls.__instance

    def __repr__(self):
        return " dEdx(<filename>)"

    def __str__(self):
        print(" dEdx parameters:")
        print("     ----> Execution date:", self.getIssueDate())
        print("    Coefficient for dE/dx:", self.getK(), \
              " ", self.getKUnit())
        print("  Effective atomic nunber:", self.getZ())
        print("    Effective mass nunber:", self.getA())
        print("                     Eta1:", self.getEta1(), \
              " ", self.getEta1Unit())
        print("          Projectile mass:", self.getProjectileMass(), \
              " ", self.getProjectileMassUnit())
        return "     <---- Done."

    
#--------  I/o methods:
    @classmethod
    def getdEdxs(cls, _filename):
        dEdxParams = pnds.read_csv(_filename)
        return dEdxParams

    
#--------  Extracting data from the WorkPackage pandas dataframe:
    @classmethod
    def parsedEdx(cls):
        Rows = cls._cntrlParams.index
        for i in Rows:
            if cls.__Debug:
                print(" dEdx: parsedEdx: processing flag: ", \
                      cls._cntrlParams.iat[i,0])
            if cls._cntrlParams.iat[i,0] == "Coefficient for dE/dx":
                K     = cls._cntrlParams.iat[i,1]
                KUnit = cls._cntrlParams.iat[i,2]
            elif cls._cntrlParams.iat[i,0].find("<Z>") >= 0:
                Z = cls._cntrlParams.iat[i,1]
            elif cls._cntrlParams.iat[i,0].find("<A>") >= 0:
                A = cls._cntrlParams.iat[i,1]
            elif cls._cntrlParams.iat[i,0] == "Charge number":
                z = cls._cntrlParams.iat[i,1]
            elif cls._cntrlParams.iat[i,0].find("Projectile mass") >= 0:
                Mp     = cls._cntrlParams.iat[i,1]
                MpUnit = cls._cntrlParams.iat[i,2]
            else:
                print("    ----> dEdx.parsedEdx: ", \
                      " unprocessed control field:", \
                      cls._cntrlParams.iat[i,0], cls._cntrlParams.iat[i,1], \
                      cls._cntrlParams.iat[i,2])

        #.. Derived constants:
        Eta1     = K * z**2 * Z/A
        Eta1Unit = "Need to work unit out"

        return K, KUnit, Z, A, z, Eta1, Eta1Unit, Mp, MpUnit


#--------  Get/set methods:
    def setIssueDate(self, _IssueDate):
        if dEdx.__Debug:
            print(" setIssueDate:", _IssueDate)
        if isinstance(_IssueDate, dt.date):
            self._IssueDate = _IssueDate
        else:
            if dEdx.__Debug:
                print("     ----> Issue date ", \
                      " raising exception")
            raise BadIssueDate()
        
    def getIssueDate(self):
        return self._IssueDate
        
    def getChargeNumber(self):
        return self._z

    def getEta1(self):
        return self._Eta1
        
    def getEta1Unit(self):
        return self._Eta1Unit
        
    def getK(self):
        return self._K
        
    def getKUnit(self):
        return self._KUnit
        
    def getZ(self):
        return self._Z
        
    def getA(self):
        return self._A
        
    def getProjectileMass(self):
        return self._Mp
        
    def getProjectileMassUnit(self):
        return self._MpUnit


#--------  Print methods:


#--------  Processing methods:
    def getdEdx(self, T=None):
        if dEdx.__Debug:
            print(" getdEdx; T:", T)
        if T==None:
            if dEdx.__Debug:
                print("     ----> T invalid, raising exception.")
            raise BadParameters()
        if not isinstance(T, float):
            if dEdx.__Debug:
                print("     ----> T invalid, raising exception.")
            raise BadParameters()
        Ans = self.getK() * self.getChargeNumber()**2 * \
               self.getZ()/self.getA() * self.getProjectileMass() \
               / 2. / T
        return Ans
    

#--------  Exceptions:
class NonExistantFile(Exception):
    pass

class BadIssueDate(Exception):
    pass

class BadParameters(Exception):
    pass
