#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 09:02:47 2019
@author: htl17
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from braggcurve_basic import bragg_vec
from braggcurve_basic import bragg_vec1
from scipy import optimize

plt.style.use('default')

## Process data file
def prePlot(filename):
     data = pd.read_csv(filename, delim_whitespace=True, names=['StN','EventN','FibreHit','Edep','RealX','RealY','RealZ','Depth','Time'], low_memory=False, skiprows=1)
     dataplot = data[['Depth','Edep']]
     dataplot=dataplot.astype(float)
     return dataplot

## Rough manual fitting for range straggling (sigma) I got from tweaking with parameters. 
def roughRange(particleType, energy):
    if(particleType == 'Proton'):
        rangeTable = np.array([[62.4,3.0],[81.3,5.0],[111.6,9.0],[136.8,13.0],[159,17.0],[188.7,23.0],[207,27.0]])         ## [Energy (MeV), Peak Depth (cm)] ##
        index = np.where(rangeTable==energy)
        return rangeTable[index[0],1][0]
    
    elif(particleType == 'Carbon'):
        rangeTable = np.array([[120.0,3.0],[155.9,5.0],[213.4,9.0],[262.3,13.0],[306.2,17.0],[346.6,21.0],[384.5,25.0],[402.8,27.0]])        ## [Energy (MeV), Peak Depth (cm)] ##
        index = np.where(rangeTable==energy)
        return rangeTable[index[0],1][0]
    
    else:
        print('Unknown Particle Type')
        return 0

## Stuck main stuff into this function
def plotEdepFit(nEvents,data='hits.dat'): 
    fig = plt.figure(figsize=(18.0,10.0))

    averageChord = 4*0.0125/np.pi # Average chord for a circle, under rough assumption most protons at close to 0 angle
                                  # Formula of average chord = 4*radius/pi, where fibre diameter is 250 micron
    numEvents = int(nEvents)
    
    data = prePlot('hits.dat')    # Data file
    depthList=[]
    eDepList=[]

    ## Processing Data File ##
    for entry in np.arange(0,len(data)):
        depthEntry = data['Depth'][entry]/10 ## Conversion from mm->cm 
        eDepEntry = data['Edep'][entry]/(numEvents*averageChord) ## Conversion from MeV->MeV/cm/particle    
        if depthEntry not in depthList: ## Find the depth values of stations
            depthList.append(depthEntry)
            eDepList.append(eDepEntry) ## If first entry for station add to eDepList 
        else:
            eDepList[-1] += eDepEntry ## If same station add to energy deposition
    
    ## Fitting Parameters (may need manual tweaking) ##
    #####
    # phi0 -- primary fluence
    # epsilon -- fraction of primary fluence contribution to tail of energy spectrum
    # r0 -- range
    # beta -- slope parameter of fluence reduction relation
    # sigma -- width of Gaussian range straggling
    #####
    
    beta = 0.012 # Value from Bortfeld paper

    r0 = (depthList[len(depthList)-1]+0.6)*1.005 # Range, from manual tweaking
    r0_lower = r0-0.02
    r0_upper = r0+0.5
    
    particle = 'Proton'
    sigmaSet_x = [roughRange(particle, 62.4),roughRange(particle,81.3),roughRange(particle,188.7),roughRange(particle, 207.0)]
    sigmaSet_y = [0.055,0.073,0.37,0.39] ## Manually fitted width values that gave good fit for specified range
    sigma = np.interp(r0,sigmaSet_x,sigmaSet_y)
    sigma_lower = sigma*0.9
    sigma_upper = sigma*1.1

    # Fitting Bortfeld equation
    popt, pcov = optimize.curve_fit(lambda z, phi0, epsilon, r0, beta, sigma: bragg_vec(z, phi0, epsilon, r0, beta, sigma), depthList, eDepList,
                                        p0=(1,0.1,r0,beta,sigma), bounds=((0,0,r0_lower,0,sigma_lower),(100,0.2,r0_upper,0.1,sigma_upper)))

    # Plotting data and fit
    colorlist = ['red','red','orange','orange','yellow','yellow','lime','lime']
    print(" ******** KL:  <--------")
    print("     ----> depthList:", depthList)
    print("     ----> eDepList:", depthList)
    for i in np.arange(0,int(len(depthList))):
        plt.errorbar(depthList[i],eDepList[i],fmt='o', color=colorlist[i],zorder=1)            

    xd = np.linspace(0,30,num=1000)
    plt.plot(xd, bragg_vec1(xd,*popt),color='black',linestyle='--',lw=2.0,zorder=0,label='Fitted Bragg Peak')
    plt.legend(fontsize=14, frameon=True, facecolor='white',framealpha=1,edgecolor='black')

    plt.title("Proton Simulation Energy Deposition",fontsize=26)
    plt.xlabel('Depth [cm]',fontsize=18)
    plt.ylabel('Edep [MeV/cm/Particle]',fontsize=18)

    fig.set_size_inches(15,8)
    fig.savefig('hits_deposition.png',transparent=False)

plotEdepFit(10000,'hits.dat')
