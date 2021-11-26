#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 11:34:42 2020

@authors: Katherine Collett and Sivapriya Bhagavathy
"""

#Import Python core modules
#import pandas as pd
import numpy as np

#import custom python modules
import analyservariables as av


class analyzer:
        def __init__(self,evData,VehicleData):
            self.evData = evData
            self.VehicleData = VehicleData
            self.s_region_series = []
            self.region_EVHistoricData = []
            
        def analyseDataforSCurveCumulative(self, region):
            region_EV1 = self.evData[region]
            region_net1 = self.VehicleData[region]
            inv_region = []
            
            self.region_EVHistoricData = [(i / j) for i, j in zip(region_EV1, region_net1)]

          
            for i in range(0,len(self.region_EVHistoricData)):
                inv_region.append(np.log(self.region_EVHistoricData[i]/(1-self.region_EVHistoricData[i])))
            [m,c] = np.polyfit(range(av.fitStart,len(self.region_EVHistoricData)),inv_region[av.fitStart:],1)
            
            #Defining function to calculate s curve series
            def scurve(x):
                st = m*x+c
                return 1/(1+np.exp(-st))

            
            for i in range(0,520):
                self.s_region_series.append(scurve(i))
                
