#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 11:32:12 2020

@authors: Katherine Collett and Sivapriya Bhagavathy
"""

#Import Python core modules
import os
import pandas as pd
import numpy as np

#Import custom modules
import dataextract
import analyzer

path=os.getcwd()
os.chdir(path)

#defining file names
netVehicleDataFile = 'veh0122.xlsx'
evDataFile = 'veh0132.xlsx'
countyDataFile = 'CountyDistricts.xlsx'
la2CountyFile = 'LA2County.xlsx'

#set year and quarter
year = "2021"
Quarter = "Q1"

#Opening files
netVehicleData = dataextract.Dataextract(netVehicleDataFile)
netVehicleData.openfile(sheet=0, sheet_type = 'xlsx')

electricVehicleData = dataextract.Dataextract(evDataFile)
electricVehicleData.openfile(sheet=2,sheet_type = 'xlsx')

countyData = dataextract.Dataextract(countyDataFile)
countyData.openfile(sheet=1,sheet_type = 'xlsx')

la2CountyData = dataextract.Dataextract(la2CountyFile)
la2CountyData.openfile(sheet=1,sheet_type = 'xlsx')

#cleaning Data
netVehicleData.cleanseVehData(countyData = countyData.rawdf)
electricVehicleData.cleanseEVData(countyData = la2CountyData.rawdf)

#analysis and prepping for csv
regions = netVehicleData.rawdf.columns
historic_data_Qs = netVehicleData.rawdf.index
test_matching = electricVehicleData.rawdf.index
if (test_matching == historic_data_Qs).all() == False:
    print("Quarters do not match")
   
data_to_save_historic = pd.DataFrame()
data_to_save_S_curve = pd.DataFrame()

index_year = 2011
index_Q = 4
S_curve_index = [None]*520
for n in range(520):
    S_curve_index[n] = f"{index_year} Q{index_Q}"
    if index_Q == 4:
        index_Q = 1
        index_year += 1
    else: index_Q += 1


for place in regions:
    sCurveData = analyzer.analyzer(electricVehicleData.rawdf,netVehicleData.rawdf)
    sCurveData.analyseDataforSCurveCumulative(place)
    
    data_to_save_historic['Quarter'] = historic_data_Qs
    header_2 = str(place + '_total_vehicles')
    data_to_save_historic[header_2] = netVehicleData.rawdf[place].values.tolist()     
    header_3 = str(place + '_EVs')
    data_to_save_historic[header_3] = electricVehicleData.rawdf[place].values.tolist()
    header_1 = str(place + '_historic_percent_EV')
    data_to_save_historic[header_1] = np.around(sCurveData.region_EVHistoricData,5)
    
    data_to_save_S_curve['Quarter'] = S_curve_index
    header_4 = str(place + '_S_curve')
    data_to_save_S_curve[header_4] = np.around(sCurveData.s_region_series, 5)

    

length = 354 #to select data until 2100 Q1
data_to_save_S_curve = data_to_save_S_curve[:length]
      
    
title_historic = "Percent_cumulative_EVs_historic_" + year + '_' +  Quarter + ".xlsx"
title_S_curve = "Percent_cumulative_EVs_S_curve_" + year + '_' +  Quarter + ".xlsx"

data_to_save_historic.to_excel(title_historic,index=False, sheet_name = year + '_' + Quarter)
data_to_save_S_curve.to_excel(title_S_curve,index=False, sheet_name = year + '_' + Quarter)

