#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 11:34:12 2020

@authors: Katherine Collett and Sivapriya Bhagavathy
"""

#Import Python core modules
import pandas as pd
import numpy as np


class Dataextract:
    
    def __init__(self,filename):
        self.filename = filename
        self.rawdf = ""
    
    def openfile(self, sheet, sheet_type):
        if sheet_type == 'xlsx':
            if sheet == 1:
                self.rawdf = pd.read_excel(self.filename)
                
            elif sheet == 2:
                rawdf = pd.read_excel(self.filename, sheet_name = None)
                rawdf_keys = list((sorted(rawdf.keys())))
                self.rawdf = rawdf[rawdf_keys[1]] #filters for second sheet only
            else: 
                self.rawdf = pd.read_excel(self.filename, sheet_name=None)
        else:
            print("ERROR! Wrong type of data file")

    def cleanseVehData(self,countyData):
        rawdf_keys = list((sorted(self.rawdf.keys())))

        county_list = countyData['County'].unique()
        county_list = np.append(county_list, "UK")
        newdf = pd.DataFrame(index=county_list) #creating an empty dataframe to store the final database
        
        for key in rawdf_keys:
            tempdf = self.rawdf[key]
            cols = list(tempdf.columns)
        
            tempdf.replace('c',0,inplace=True)
            tempdf[cols[0]].replace('     ', np.nan, inplace=True)
            tempdf.fillna(0,inplace=True)
            
            idx = tempdf.index[tempdf[cols[0]].str.contains("Post", na=False)]
            tempdf.drop(tempdf.head(idx[0]+1).index,inplace = True)
            
            idx = tempdf.index[tempdf[cols[0]]==0]
            tail = tempdf.index[-1]-idx[0]+1
            tempdf.drop(tempdf.tail(tail).index, inplace=True)  
            
            tempdf = tempdf.loc[:, (tempdf != 0).any(axis=0)] #drops any columns that are all zero
            cols = list(tempdf.columns)
            
            PostCodes = tempdf[cols[0]]
            tempdf2 = pd.DataFrame(index = PostCodes)
            n = range(len(PostCodes))
            
            ii = 0
            number_Qs = int((len(tempdf.columns)-1)/3)
            for n, row in tempdf.iterrows():
                for i in range(0, number_Qs):
                    colname = (key+" Q"+str(i+1))
                    tempdf2.loc[PostCodes.iloc[ii],colname] = row[cols[3*i+1]]+row[cols[3*i+2]]+row[cols[3*i+3]]
                ii +=1
            
            Veh_UK = pd.DataFrame()
            Veh_UK['UK'] = tempdf2.sum()
            Veh_UK = Veh_UK.T
            tempdf2 = tempdf2.reset_index()

                    
            df_merge = pd.merge(tempdf2,countyData,left_on = cols[0],right_on = 'Postcode_District')
            delete = [cols[0], 'Postcode_District']
            df_merge = df_merge.drop(columns = delete)
            tempdf3 = pd.DataFrame()
            tempdf3 = df_merge.groupby('County').apply(lambda x: x.astype(int).sum())
            tempdf3 = tempdf3.append(Veh_UK)
            newdf = pd.concat([newdf, tempdf3], axis=1, sort = True)
                     
        newdf.drop(newdf.columns[[0,1,2,3,4,5,6]], axis=1, inplace=True)
        
        self.rawdf = newdf.T
        
    def cleanseEVData(self,countyData):
        self.rawdf.replace('c',0,inplace=True)
        self.rawdf.fillna(0,inplace=True)
        cols_ev = list(self.rawdf.columns)
        idx = self.rawdf.index[self.rawdf[cols_ev[0]].str.contains("ONS LA", na=False)] #identify column headings
        new_columns = self.rawdf.loc[idx,:].values.tolist()
        self.rawdf.set_axis(new_columns[0], axis='columns')
        cols_ev = list(self.rawdf.columns)
        self.rawdf.drop(self.rawdf.head(idx[0]+1).index,inplace = True) #delete data under column headings
        idx = self.rawdf.index[self.rawdf[cols_ev[1]]==0] #index with 0 in region column
        tail = self.rawdf.index[-1]-idx[0]+1
        self.rawdf.drop(self.rawdf.tail(tail).index, inplace=True) #drops rows with 0 in region column
        self.rawdf[cols_ev[1]]=self.rawdf[cols_ev[1]].str.lstrip() #strips leading and trailing space characters

        EV_UK = self.rawdf.loc[self.rawdf[cols_ev[1]].str.contains("United Kingdom")]
        EV_UK = EV_UK.drop(columns = cols_ev[:2])
        UK = ['UK']
        EV_UK.set_axis(UK, axis='index')
        
        
        df_merge = pd.merge(self.rawdf,countyData,left_on = cols_ev[0],right_on = 'ONS LA Code') #replace region with county code
        self.rawdf = df_merge.groupby('County Name')[cols_ev[2:]].apply(lambda x: x.astype(int).sum()) #group by county

        self.rawdf = self.rawdf.append(EV_UK)
        
        columns = self.rawdf.columns.tolist()
        columns = columns[::-1] 
        self.rawdf = self.rawdf[columns] #reverses the order of all the data so the columns are now ordered oldest to most recent
        self.rawdf = self.rawdf.replace(0, 1)
        
        
        self.rawdf = self.rawdf.T #transpose

