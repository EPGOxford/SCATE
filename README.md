Readme file for SCATE, the S-Curve Adoption Tool for Electric Vehicles, available on GitHub at: https://github.com/EPGOxford/SCATE

# S-Curve Adoption Tool For Electric Vehicles (SCATE)

## Overview
SCATE is the S-Curve Adoption Tool for Electric Vehicles developed by the University of Oxford's Energy and Power Group. SCATE is designed to use historic data of electric vehicle (EV) adoption to forecast future adoption. This transforms the historic data into useful future insights for planning. Policy makers, local authorities, businesses, and academics can all benefit from using S-curve data in their analyses and planning for the increasing number of electric vehicles.

In this instance, S-curves are forecast for English Counties using data from the UK Government’s Department for Transport.

## Running SCATE
To operate SCATE, download the source code.

We recommend creating a new virtual environment from the requirements.txt file. This can be done using pip install or conda as follows, where `<env_name>` is replaced with the name of your new environment:
```
python3 -m venv <env_name>
source <env_name>/bin/activate
cd <directory of source code>
python3 -m pip install -r requirements.txt
```
or
```
conda create --name <env_name> --file requirements.txt
```
Once your new environment is created with the necessary packages, simply run 'main.py'.

## File Descriptions

### Source Code and Input Files

**main.py** is the primary script to be run in python. This is where the files containing the primary data and look-up tables described below are defined and the analysis period for SCATE is set. This file then calls on other sub-modules to re-structure the primary data and to perform the S-curve analysis. 

**dataextract.py** is a sub-module to main.py. This module extracts data from the primary data sources and uses the look-up tables to group the historic data by County. 

**analyser.py** is a sub-module to main.py. When this module Is called, the S-curve analysis is conducted, to assess future adoption of EVs in each County. 

**analyservaribales.py** is a sub-module to main.py. This file defines variables necessary for analyser.py to run. 

**LA2County.xlsx** is the look-up table for Local Authority to County. UK Government’s Office for National statistics provided data from which the look-up table for local authorities within England to Counties was created. Available at: https://geoportal.statistics.gov.uk

**CountyDistricts.xlsx** is the look-up table for Postcode District to County. The look-up table for postcode districts within each English County was developed from data available for download at: https://www.doogal.co.uk/counties.php

**veh0132.xlsx** and **veh0122.xlsx** are the primary input data files from the UK Government’s Department for Transport. They contain data on the number of battery electric vehicles (Table VEH0132b) and the number of licenced vehicles (Table VEH0122) for the UK from 2011 Q4 to 2021 Q1. They are available at: 
https://www.gov.uk/government/collections/transport-statistics-great-britain used in line with the Open Goverment Licence https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/

**requirements.py** lists the necessary python packages and their versions, in order to set up a new virtual environment.

### Example output data
**Percent_cumulative_EVs_historic_2021_Q1.xlsx** is the historic data. This includes the total number of vehicles, the number of electric vehicles (EVs), and the historic percent of vehicles which are EV for each quarter (between 2011 Q4 and 2021 Q1) in each County.

**Percent_cumulative_EVs_S_curve_2021_Q1.xlsx** is the S-curve data. This shows the forecast S-curve data based on the historic data for each County up to 2100 Q1. 

## Copyright
SCATE © Copyright, Energy and Power Group, University of Oxford 2021. All Rights Reserved. 
The authors, being Dr Katherine A. Collett and Dr Sivapriya Mothilal Bhagavathy have asserted their moral rights.

