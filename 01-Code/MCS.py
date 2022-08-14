#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class MCS:
==========

  Calculates the MCS effect for a variety of situations.  Use singleton
  class so that instance attributes can be used to set the parameters.


  Class attributes:
  -----------------
  __instance : Set on creation of first (and only) instance.
  __Debug    : boolean ... debug flag      

  Instance attributes:
  --------------------
   __filename  = Filename from which parameters have been read.  If None
                 then default values are used.
   _MCSParams  = Pandas data frame instance containing parameters
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
import math   as mth
import pandas as pnds
from datetime import date

class MCS(object):
    __instance = None
    __Debug    = False

#--------  "Built-in methods":
    def __new__(cls, _filename=None):

        if cls.__instance is None:
            cls.__instance = super(MCS, cls).__new__(cls)
        
            if _filename == None:
                if  MCS.__Debug:
                    print(" MCS: no filename provided, take defaults.")
            elif not os.path.isfile(_filename):
                print(" MCS: file ", _filename, " does not exist.", \
                      " Raising exception")
                raise NonExistantFile('CSV file' + \
                                      _Filename + \
                                      ' does not exist; execution termimated.')

            #.. Set defaults:
            cls._filename  = None
            cls._IssueDate = date.today()
            cls._MCSParams = None

            #.. Parse control file:
            if _filename != None:
                cls._cntrlParams = cls.getMCSs(_filename)
                if cls.__Debug:
                    print(" MCS: control parameters: \n", \
                          cls._cntrlParams)
                cls._IonE, cls._IonEUnit, \
                cls._z, \
                cls._X0, cls._X0Unit, \
                cls._rho, cls._rhoUnit, \
                cls._Mp, cls._MpUnit, \
                cls._Eta1, cls._Eta1Unit, \
                cls._Alpha1, cls._Alpha1Unit = cls.parseMCS()
        
        return cls.__instance

    def __repr__(self):
        return " MCS(<filename>)"

    def __str__(self):
        print(" MCS parameters:")
        print("     ----> Execution date:", self.getIssueDate())
        print("        Ionisation energy:", self.getIonisationEnergy(), \
              " ", self.getIonisationEnergyUnit())
        print(" Projectile charge number:", self.getChargeNumber())
        print("                       X0:", self.getX0(), \
              " ", self.getX0Unit())
        print("                  Density:", self.getrho(), \
              " ", self.getrhoUnit())
        print("         Radiation length:", self.getRadiationLength(), \
              " ", self.getRadiationLengthUnit())
        print("          Projectile mass:", self.getProjectileMass(), \
              " ", self.getProjectileMassUnit())
        print("        Derived constants: \n", \
              "            ----> Eta1   =", self.getEta1(), \
              self.getEta1Unit(), "\n", \
              "            ----> Alpha1 =", self.getAlpha1(), \
              self.getAlpha1Unit())
        return "     <---- Done."

    
#--------  I/o methods:
    @classmethod
    def getMCSs(cls, _filename):
        MCSParams = pnds.read_csv(_filename)
        return MCSParams

    
#--------  Extracting data from the WorkPackage pandas dataframe:
    @classmethod
    def parseMCS(cls):
        Rows = cls._cntrlParams.index
        for i in Rows:
            if cls.__Debug:
                print(" MCS: parseMCS: processing flag: ", \
                      cls._cntrlParams.iat[i,0])
            if cls._cntrlParams.iat[i,0] == "Ionisation energy":
                IonE     = cls._cntrlParams.iat[i,1]
                IonEUnit = cls._cntrlParams.iat[i,2]
            elif cls._cntrlParams.iat[i,0] == "Charge number":
                z = cls._cntrlParams.iat[i,1]
            elif cls._cntrlParams.iat[i,0].find("Radiation length") >= 0:
                X0     = cls._cntrlParams.iat[i,1]
                X0Unit = cls._cntrlParams.iat[i,2]
            elif cls._cntrlParams.iat[i,0].find("Density") >= 0:
                rho     = cls._cntrlParams.iat[i,1]
                rhoUnit = cls._cntrlParams.iat[i,2]
            elif cls._cntrlParams.iat[i,0].find("Projectile mass") >= 0:
                Mp     = cls._cntrlParams.iat[i,1]
                MpUnit = cls._cntrlParams.iat[i,2]
            else:
                print("    ----> MCS.parseMCS: ", \
                      " unprocessed control field:", \
                      cls._cntrlParams.iat[i,0], cls._cntrlParams.iat[i,1], \
                      cls._cntrlParams.iat[i,2])

        #.. Derived constants:
        Eta1       = IonE * z / (2. * mth.sqrt(X0/rho))
        Eta1Unit   = "Need to work out unit!"
        Alpha1     = z**2 * Mp / (2. * X0/rho)
        Alpha1Unit = "Need to work out unit!"
            

        return IonE, IonEUnit, z, X0, X0Unit, rho, rhoUnit, Mp, MpUnit, \
               Eta1, Eta1Unit, Alpha1, Alpha1Unit


#--------  Get/set methods:
    def setIssueDate(self, _IssueDate):
        if MCS.__Debug:
            print(" setIssueDate:", _IssueDate)
        if isinstance(_IssueDate, dt.date):
            self._IssueDate = _IssueDate
        else:
            if MCS.__Debug:
                print("     ----> Issue date ", \
                      " raising exception")
            raise BadIssueDate()
        
    def getIssueDate(self):
        return self._IssueDate
        
    def getIonisationEnergy(self):
        return self._IonE
        
    def getIonisationEnergyUnit(self):
        return self._IonEUnit
        
    def getChargeNumber(self):
        return self._z

    def getX0(self):
        return self._X0
    
    def getX0Unit(self):
        return self._X0Unit
    
    def getrho(self):
        return self._rho
    
    def getrhoUnit(self):
        return self._rhoUnit
    
    def getRadiationLength(self):
        return self._X0*self._rho
        
    def getRadiationLengthUnit(self):
        RtnStr = self._X0Unit + " <devide> " + self._rhoUnit
        return RtnStr
        
    def getProjectileMass(self):
        return self._Mp
        
    def getProjectileMassUnit(self):
        return self._MpUnit

    def getEta1(self):
        return self._Eta1

    def getEta1Unit(self):
        return self._Eta1Unit

    def getAlpha1(self):
        return self._Alpha1
        
    def getAlpha1Unit(self):
        return self._Alpha1Unit
        

#--------  Print methods:


#--------  Processing methods:
    def getTheta0(self, x=None, T=None):
        if MCS.__Debug:
            print(" getTheta0; x and T:", x, T)
        if x==None or T==None:
            if MCS.__Debug:
                print("     ----> x or T invalid, raising exception.")
            raise BadParameters()
        if not (isinstance(x, float) or isinstance(T, float)):
            if MCS.__Debug:
                print("     ----> x or T invalid, raising exception.")
            raise BadParameters()
        sqrtx = mth.sqrt(x)
        Theta0 = self.getEta1() * (sqrtx / T) * \
                 (1. + 0.038*mth.log(self.getAlpha1()*x/T))
        if MCS.__Debug:
            print("     ----> Theta0:", Theta0)
        return Theta0

    def getYplane(self, x=None, T=None):
        if MCS.__Debug:
            print(" getYPlane; x and T:", x, T)
        Yplane = (x / mth.sqrt(3)) * self.getTheta0(x, T)
        if MCS.__Debug:
            print("     ----> Yplane:", Yplane)
        return Yplane


#--------  Exceptions:
class NonExistantFile(Exception):
    pass

class BadIssueDate(Exception):
    pass

class BadParameters(Exception):
    pass
