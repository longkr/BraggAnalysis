#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 11:58:21 2019

@author: htl17
"""

import math  as mth
import numpy as np
from scipy import special

import MCS as mcs

################
## Parameters ##
################
# Exponent of range-energy relation
p = 1.77

# Fraction of locally absorbed energy released in 
# nonelastic nuclear interactions
gamma = 0.6
#https://aapm.onlinelibrary.wiley.com/doi/abs/10.1118/1.4956280

# Proportionality factor [cm MeV^{-p}]
alpha = 0.0022

# Density of water [g/cm^3]
rho = 1.0

########################################
## Components of Bragg Analytic Curve ##
########################################
def prebragg(z, phi0, epsilon, r0, beta):
    return phi0/(rho*p*alpha**(1/p)*(1+beta*r0))*((r0-z)**(1/p - 1) 
                 + (beta + gamma*beta*p + epsilon*p/r0)*(r0-z)**(1/p))

def peak(z, phi0, epsilon, r0, beta, sigma):
    xi = (r0-z)/sigma
    factorial = 1.57539 # Factorial component (1/p -1)! calculated in Mathematica
    prefactor = phi0*((np.exp(-(xi**2/4))*sigma**(1/p)*factorial)
    /(np.sqrt(2*np.pi)*rho*p*alpha**(1/p)*(1+beta*r0)))
    return prefactor*(1/sigma * special.pbdv(-1/p, -xi)[0] 
                      + (beta/p + gamma*beta + epsilon/r0)*special.pbdv((-1/p)-1,-xi)[0])
    
def bragg(z, phi0, epsilon, r0, beta, sigma):
    if z < (r0-10*sigma):
        return prebragg(z, phi0, epsilon, r0, beta)
    elif np.logical_and(z >= (r0-10*sigma), z<= (r0+5*sigma)):
        return peak(z, phi0, epsilon, r0, beta, sigma)
    else:
        return 0  
    
def bragg_vec(z, phi0, epsilon, r0, beta, sigma):
    y = np.zeros(z.shape)
    for i in range(len(y)):
        y[i]=bragg(z[i], phi0, epsilon, r0, beta, sigma)
            
    return y

def bragg_vec1(z, phi0, epsilon, r0, beta, sigma):
    y = np.zeros(z.shape)
    iMCS = mcs.MCS('../11-BraggParameters/BraggParameters.csv')
    zi = -0.03003003003003
    yPlni = 0.
    print("z, dz, T, yPln, dV, yi, y, E, p, relbeta, relgamma, ", \
          "relgamma*relbeta")
    for i in range(len(y)):
        y[i]=bragg(z[i], phi0, epsilon, r0, beta, sigma)
        if (r0-z[i]) > 0.:
            T  = ( (r0-z[i]) / alpha )**(1./p)
            Ti = T
        T = Ti
        dz   = (z[i]-zi)
        if dz != 0. and T > 115.:
            yPln  = iMCS.getYplane(dz, T)
            yPlni = yPln
        dz   = (z[i]-zi)
        yPln = yPlni
        dV    = np.pi*(0.1 + yPln)**2 * dz
        yi   = y[i]
        y[i] = y[i] / dV
        Energy   = iMCS.getProjectileMass() + T
        mmtm     = mth.sqrt(Energy**2 - iMCS.getProjectileMass()**2)
        relbeta  = mmtm/Energy
        relgamma = 1./mth.sqrt(1.-relbeta**2)
        print(z[i], dz, T, yPln, dV, yi, y[i], Energy, mmtm, \
              relbeta, relgamma, relgamma*relbeta)
        zi   = z[i]
            
    return y

def zeta(r0, sigma, z):
    return (z-r0)/sigma

def xi(r0,R0,sigma,z):
    return (z-r0-R0)/sigma

def tParabolicCylinderD(r0,R0,sigma,v,z):
    return np.exp(-(xi(r0,R0,sigma,z)**2)/4)*special.pbdv(v,xi(r0,R0,sigma,z))[0]-np.exp(-(zeta(r0,sigma,z)**2)/4)*special.pbdv(v,zeta(r0,sigma,z))[0]

def fluence(phi,sigma,r0,z):
    return phi/np.sqrt(2*np.pi)*np.exp(-(zeta(r0,sigma,z))**2/4)*special.pbdv(-1,zeta(r0,sigma,z))[0]
