#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class Bortfeldt:
===========

  Calculates the Bortfeldt effect for a variety of situations.  Use singleton
  class so that instance attributes can be used to set the parameters.


  Class attributes:
  -----------------
  __instance : Set on creation of first (and only) instance.
  __Debug    : boolean ... debug flag      

  Instance attributes:
  --------------------
   __filename  = Filename from which parameters have been read.  If None
                 then default values are used.
   _BortfeldtParams  = Pandas data frame instance containing parameters
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

class Bortfeldt(object):
    __instance = None
    __Debug    = True

#--------  "Built-in methods":
    def __new__(cls, _filename=None):

        if cls.__instance is None:
            cls.__instance = super(Bortfeldt, cls).__new__(cls)
        
            if _filename == None:
                if  Bortfeldt.__Debug:
                    print(" Bortfeldt: no filename provided, take defaults.")
            elif not os.path.isfile(_filename):
                print(" Bortfeldt: file ", _filename, " does not exist.", \
                      " Raising exception")
                raise NonExistantFile('CSV file' + \
                                      _filename + \
                                      ' does not exist; execution termimated.')

            #.. Set defaults:
            cls._filename  = None
            cls._IssueDate = date.today()
            cls._BortfeldtParams = None

            #.. Parse control file:
            if _filename != None:
                cls._cntrlParams = cls.getBortfeldts(_filename)
                if cls.__Debug:
                    print(" Bortfeldt: parameters: \n", \
                          cls._cntrlParams)
                cls._p, cls._gamma, cls._alpha, cls._alphaUnit, \
                    cls._rho, cls._rhoUnit \
                    = cls.parseBortfeldt()
        
        return cls.__instance

    def __repr__(self):
        return " Bortfeldt(<filename>)"

    def __str__(self):
        print(" Bortfeldt parameters:")
        print("     ----> Execution date:", self.getIssueDate())
        print(" Exponent of range-energy relation:", self.getRangeEnergy())
        print("               Nonelastic fraction:", self.getNonElasFrac())
        print("            Proportionality factor:", self.getalpha(), \
              " ", self.getalphaUnit())
        print("                           Density:", self.getrho(), \
              " ", self.getrhoUnit())
        return "     <---- Done."

    
#--------  I/o methods:
    @classmethod
    def getBortfeldts(cls, _filename):
        BortfeldtParams = pnds.read_csv(_filename)
        return BortfeldtParams

    
#--------  Extracting data from the WorkPackage pandas dataframe:
    @classmethod
    def parseBortfeldt(cls):
        Rows = cls._cntrlParams.index
        for i in Rows:
            if cls.__Debug:
                print(" Bortfeldt: parseBortfeldt: processing flag: ", \
                      cls._cntrlParams.iat[i,0])
            if cls._cntrlParams.iat[i,0].find("range-energy") >= 0:
                p = cls._cntrlParams.iat[i,1]
            elif cls._cntrlParams.iat[i,0].find("nonelastic nuc") >= 0:
                gamma = cls._cntrlParams.iat[i,1]
            elif cls._cntrlParams.iat[i,0].find("Proportionality factor") >= 0:
                alpha     = cls._cntrlParams.iat[i,1]
                alphaUnit = cls._cntrlParams.iat[i,2]
            elif cls._cntrlParams.iat[i,0].find("Density") >= 0:
                rho     = cls._cntrlParams.iat[i,1]
                rhoUnit = cls._cntrlParams.iat[i,2]
            else:
                print("    ----> Bortfeldt.parseBortfeldt: ", \
                      " unprocessed control field:", \
                      cls._cntrlParams.iat[i,0], cls._cntrlParams.iat[i,1], \
                      cls._cntrlParams.iat[i,2])

        #.. Derived constants:

        return p, gamma, alpha, alphaUnit, rho, rhoUnit


#--------  Get/set methods:
    def setIssueDate(self, _IssueDate):
        if self.__Debug:
            print(" setIssueDate:", _IssueDate)
        if isinstance(_IssueDate, dt.date):
            self._IssueDate = _IssueDate
        else:
            if self.__Debug:
                print("     ----> Issue date ", \
                      " raising exception")
            raise BadIssueDate()
        
    def getIssueDate(self):
        return self._IssueDate
        
    def getRangeEnergy(self):
        return self._p

    def getNonElasFrac(self):
        return self._gamma
        
    def getalpha(self):
        return self._alpha
        
    def getalphaUnit(self):
        return self._alphaUnit
        
    def getrho(self):
        return self._rho
    
    def getrhoUnit(self):
        return self._rhoUnit
        

#--------  Print methods:


#--------  Processing methods:
    def getBortfeldt(self, T=None):
        if self.__Debug:
            print(" getBortfeldt; T:", T)
        if T==None:
            if self.__Debug:
                print("     ----> T invalid, raising exception.")
            raise BadParameters()
        if not isinstance(T, float):
            if self.__Debug:
                print("     ----> T invalid, raising exception.")
            raise BadParameters()

        Bortfeldt = 0.
        
        return Bortfeldt
    
    ########################################
    ## Components of Bragg Analytic Curve ##
    ########################################
    def prebragg(self, z, phi0, epsilon, r0, beta):
        rho = self._rho
        p   = self._p
        alpha = self._alpha
        gamma = self._gamma
        
        return phi0/(rho*p*alpha**(1/p)*(1+beta*r0))*((r0-z)**(1/p - 1) \
               + (beta + gamma*beta*p + epsilon*p/r0)*(r0-z)**(1/p))

    def peak(self, z, phi0, epsilon, r0, beta, sigma):
        rho = self._rho
        p   = self._p
        alpha = self._alpha
        gamma = self._gamma

        xi = (r0-z)/sigma
        factorial = 1.57539 # Factorial component (1/p -1)!
                            # calculated in Mathematica
        prefactor = phi0*((np.exp(-(xi**2/4))*sigma**(1/p)*factorial) \
                    /(np.sqrt(2*np.pi)*rho*p*alpha**(1/p)*(1+beta*r0)))
        return prefactor*(1/sigma * special.pbdv(-1/p, -xi)[0] 
               + (beta/p + gamma*beta + \
                  epsilon/r0)*special.pbdv((-1/p)-1,-xi)[0])
    
    def bragg(self, z, phi0, epsilon, r0, beta, sigma):
        rho = self._rho
        p   = self._p
        alpha = self._alpha
        gamma = self._gamma

        if z < (r0-10*sigma):
            return prebragg(z, phi0, epsilon, r0, beta)
        elif np.logical_and(z >= (r0-10*sigma), z<= (r0+5*sigma)):
            return peak(z, phi0, epsilon, r0, beta, sigma)
        else:
            return 0  
    
        def bragg_vec(self, z, phi0, epsilon, r0, beta, sigma):
            y = np.zeros(z.shape)
            for i in range(len(y)):
                y[i]=bragg(z[i], phi0, epsilon, r0, beta, sigma)
            return y

        def zeta(self, r0, sigma, z):
            return (z-r0)/sigma

        def xi(self, r0,R0,sigma,z):
            return (z-r0-R0)/sigma

        def tParabolicCylinderD(self, r0,R0,sigma,v,z):
            return np.exp(-(xi(r0,R0,sigma,z)**2)/4)* \
                special.pbdv(v,xi(r0,R0,sigma,z))[0]-\
                np.exp(-(zeta(r0,sigma,z)**2)/4)*\
                special.pbdv(v,zeta(r0,sigma,z))[0]

        def fluence(self, phi,sigma,r0,z):
            return phi/np.sqrt(2*np.pi)*np.exp(-(zeta(r0,sigma,z))**2/4)*\
                special.pbdv(-1,zeta(r0,sigma,z))[0]

#--------  Exceptions:
class NonExistantFile(Exception):
    pass

class BadIssueDate(Exception):
    pass

class BadParameters(Exception):
    pass
