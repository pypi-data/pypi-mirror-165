# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 09:50:00 2019

@author: michaelek
"""
from thinsos import SOS
import pandas as pd

pd.options.display.max_columns = 10

###################################
### Parameters

url1 = 'http://sensorweb.demo.52north.org/sensorwebtestbed/service'

foi1 = 'Vaisala-WXT520'
observed_property1 = 'WindSpeedAverage'

from_date1 = '2015-07-01'
to_date1 = '2015-07-02'

url2 = 'https://climate-sos.niwa.co.nz'

foi2 = '17244'
observed_property2 = 'MTHLY_STATS: TOTAL RAINFALL (MTHLY: TOTAL RAIN)'

from_date2 = '2018-06-01'
to_date2 = '2018-10-01'

bbox = [[169, -45.5], [174.2, -41.7]]
#bbox = [[0, 0], [60, 60]]

###################################
### Tests

## 52 North test server

def test_sos1():
    sos1 = SOS(url1)

    assert isinstance(sos1.capabilities, dict) & isinstance(sos1.data_availability, pd.DataFrame) & (len(sos1.capabilities) == 8) & (len(sos1.data_availability) > 40)

sos1 = SOS(url1)

def test_get_foi1():
    foi_df1 = sos1.get_foi()

    assert isinstance(foi_df1, pd.DataFrame) & (len(foi_df1) >= 4)

def test_get_observation1():
    obs_df1 = sos1.get_observation(foi1, observed_property1, from_date=from_date1, to_date=to_date1)

    assert isinstance(obs_df1, pd.DataFrame) & (len(obs_df1) >= 90)


## NIWA climate server

def test_sos2():
    sos2 = SOS(url2)

    assert isinstance(sos2.capabilities, dict) & isinstance(sos2.data_availability, pd.DataFrame) & (len(sos2.capabilities) == 8) & (len(sos2.data_availability) > 3000)

sos2 = SOS(url2)

def test_get_foi2():
    foi_df2 = sos2.get_foi(bbox=bbox)

    assert isinstance(foi_df2, pd.DataFrame) & (len(foi_df2) >= 20)

def test_get_observation2a():
    obs_df2 = sos2.get_observation(foi2, observed_property2, from_date=from_date2, to_date=to_date2)

    assert isinstance(obs_df2, pd.DataFrame) & (len(obs_df2) == 5)

def test_get_observation2b():
    obs_df3 = sos2.get_observation(foi2, observed_property2)

    assert isinstance(obs_df3, pd.DataFrame) & (len(obs_df3) > 200)



