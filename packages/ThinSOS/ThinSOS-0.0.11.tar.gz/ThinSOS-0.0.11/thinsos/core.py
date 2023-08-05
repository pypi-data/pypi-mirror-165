# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 09:39:12 2019

@author: michaelek
"""

import requests
import pandas as pd
from time import sleep
import urllib.parse

#############################################################
### Functions


def foi_parse(foi_dict):
    """

    """
    foi_dict1 = foi_dict.copy()
    if isinstance(foi_dict1['identifier'], dict):
        foi_dict1.update({'identifier': foi_dict1['identifier']['value']})
    foi_dict1.update({'lat': foi_dict1['geometry']['coordinates'][0], 'lon': foi_dict['geometry']['coordinates'][1]})
    foi_dict1.pop('geometry')

    return foi_dict1


def obs_parse_iter(obs_dict):
    """

    """
    obs_dict1 = obs_dict.copy()
    obs_dict2 = foi_parse(obs_dict['featureOfInterest'])
    obs_dict1.update(obs_dict2)
    obs_dict1.pop('featureOfInterest')
    # obs_dict1.pop('phenomenonTime')

    obs_dict1.update({'result': obs_dict1['result']['value'], 'uom': obs_dict1['result']['uom']})

    return obs_dict1


def obs_parse_bulk(obs_dict):
    """

    """
    obs_dict1 = obs_dict.copy()
    obs_dict2 = foi_parse(obs_dict['featureOfInterest'])
    obs_dict1.update(obs_dict2)
    obs_dict1.pop('featureOfInterest')

    obs_dict1['uom'] = obs_dict1['result']['fields'][1]['uom']
    values = obs_dict1['result']['values']
    obs_dict1.pop('phenomenonTime')
    obs_dict1.pop('result')

    lst1 = []
    for v in values:
        new_dict1 = obs_dict1.copy()
        new_dict1.update({'resultTime': v[0], 'result': v[1]})
        lst1.append(new_dict1)

    return lst1


def obs_process(obs_list):
    """

    """
    if 'values' in obs_list[0]['result']:
        lst1 = []
        [lst1.extend(obs_parse_bulk(j)) for j in obs_list if isinstance(j, dict)]
    else:
        lst1 = [obs_parse_iter(j) for j in obs_list if isinstance(j, dict)]

    df1 = pd.DataFrame(lst1)
    df1['resultTime'] = pd.to_datetime(df1['resultTime'])
    if 'phenomenonTime' in df1:
        df1['phenomenonTime'] = pd.to_datetime(df1['phenomenonTime'])

    return df1


#def send_request(body, url, token):
#    """
#    Sends a request to a SOS using POST method.
#
#    Parameters
#    -----------
#    body : dict
#        body of the request.
#    token: str
#        Authorization Token for an existing SOS.
#    url: str
#        URL to the endpoint where the SOS can be accessed
#
#    Returns
#    -------
#    requests response
#        Server response to response formatted as JSON
#    """
#
#
##    headers = {'Authorization': str(token), 'Accept': 'application/json'}
#    body.update({'responseFormat': 'application/json'})
##    response = requests.post(url, headers=headers, data=body)
#    response = requests.get(url, params=body)
#
#    response.raise_for_status()  # raise HTTP errors
#
#    return response


######################################
### Main class


class SOS(object):
    """
    SOS class specifically for 52 North SOS. Initialised with a url string.
    """
    def __init__(self, url, token=''):
        """

        """
        self.url = url
        self.token = str(token)
        self.headers = {'Authorization': str(token), 'Accept': 'application/json'}
        self.body_base = {"service": "SOS", "version": "2.0.0"}
        self.capabilities = self.get_capabilities()
        self.data_availability = self.get_data_availability()
#        self.foi = self.get_foi()


    def _url_convert(self, body):
        """
        Sends a request to a SOS using GET method.

        Parameters
        -----------
        body : dict
            body of the request.
        url: str
            URL to the endpoint where the SOS can be accessed

        Returns
        -------
        requests response
            Server response to response formatted as JSON
        """
        # new_body = [k+'='+body[k] for k in body]
        new_body = urllib.parse.urlencode(body, quote_via=urllib.parse.quote)

        if self.url.endswith('/'):
            url = self.url[:-1]
        new_url = url + '/?' + new_body

        return new_url


    def filters(self, foi=None, procedure=None, observed_property=None, from_date=None, to_date=None):
        """

        """
        da1 = self.data_availability.copy()
        body = self.body_base.copy()

        if isinstance(foi, str):
            da1 = da1[da1.featureOfInterest == foi]
            if da1.empty:
                raise ValueError('foi does not exist')
            body.update({'featureOfInterest': foi})
        if isinstance(observed_property, str):
            da1 = da1[da1.observedProperty == observed_property]
            if da1.empty:
                raise ValueError('observedProperty does not exist')
            body.update({'observedProperty': observed_property})
        if isinstance(procedure, str):
            da1 = da1[da1.procedure == procedure]
            if da1.empty:
                raise ValueError('procedure does not exist')
            body.update({'procedure': procedure})
        if self.request == 'GetObservation':
            if isinstance(from_date, str):
                from_date1 = pd.Timestamp(from_date).isoformat() + 'Z'
            else:
                from_date1 = da1.fromDate.min().strftime('%Y-%m-%dT%H:%M:%SZ')
            if isinstance(to_date, str):
                to_date1 = pd.Timestamp(to_date).isoformat() + 'Z'
            else:
                to_date1 = da1.toDate.min().strftime('%Y-%m-%dT%H:%M:%SZ')

#            tf = {"temporalFilter": {
#                    "during": {
#                        "ref": "om:phenomenonTime",
#                        "value": [
#                            from_date1,
#                            to_date1
#                            ]
#                        }
#                    }
#                }
            tf = {"temporalFilter": "om:phenomenonTime," + from_date1 + '/' + to_date1}
            body.update(tf)
#        if isinstance(bbox, list):
#            sf = {'spatialFilter': {
#                    'bbox': {
#                            "ref": "om:featureOfInterest/sams:SF_SpatialSamplingFeature/sams:shape",
#                            'lowerCorner': bbox[0],
#                            'upperCorner': bbox[1]
#                            }
#                    }
#                }
#            body.update(sf)

        return body



    def get_capabilities(self, level='all'):
        """
        Retrives the capabilites of an existing SOS, formatted as JSON.

        Parameters
        ----------
        level: str
            Level of details in the capabilities of an SOS. Possible values: 'service', 'content', 'operations', 'all', and 'minimal'.

        Returns
        -------
        Capabilities of an SOS formatted as JSON
        """

        # classified level of detail based by requesting selected sections
        section_levels = {"service": [
            "ServiceIdentification", "ServiceProvider"
            ],
            "content": ["Contents"],
            "operations": ["OperationsMetadata"],
            "all": [
                "ServiceIdentification",
                "ServiceProvider",
                "OperationsMetadata",
                "FilterCapabilities",
                "Contents"
            ]
        }

        # Test for valid values for 'level' parameter:
        valid_levels = ['service', 'content', 'operations', 'all', 'minimal']
        if level in valid_levels:  # if parameter is in valid_levels

            if level != 'minimal':
                request_body = {"request": "GetCapabilities",
                                "sections": ','.join(section_levels[level])
                                }
            else:  # for level 'minimal'
                request_body = {"request": "GetCapabilities",
                                }

            body = self.body_base.copy()
            body.update(request_body)

            new_url = self._url_convert(body)

            response = requests.get(new_url, headers=self.headers)

            try:
                response.raise_for_status()  # raise HTTP errors
                json1 = response.json()
            except Exception as err:
                print(err)
                return response

            return json1

        else: # When no level input value matches
            print('--->> Error: The value for the "level" parameter is not valid!!')
            print("------>>> Valid values are: 'service', 'content', 'operations', 'all', and 'minimal'")
            return None


    def get_data_availability(self, foi=None, procedure=None, observed_property=None):
        """

        """
        if (foi is None) & (procedure is None) & (observed_property is None):
            body = self.body_base.copy()
        else:
            body = self.filters(foi, procedure, observed_property)
        body.update({'request': 'GetDataAvailability'})

        new_url = self._url_convert(body)

        response = requests.get(new_url, headers=self.headers)

        try:
            response.raise_for_status()  # raise HTTP errors
            json1 = response.json()['dataAvailability']
        except Exception as err:
            print(err)
            return response

        df1 = pd.DataFrame(json1)
        df1[['fromDate', 'toDate']] = pd.DataFrame(df1['phenomenonTime'].values.tolist(), columns=['fromDate', 'toDate'])
        df1.fromDate = pd.to_datetime(df1.fromDate)
        df1.toDate = pd.to_datetime(df1.toDate)

        return df1.drop('phenomenonTime', axis=1)


    def get_foi(self, foi=None, bbox=None):
        """

        """
        if (foi is None):
            body = self.body_base.copy()
        else:
            body = self.filters(foi)
        body.update({'request': 'GetFeatureOfInterest'})

        new_url = self._url_convert(body)

        response = requests.get(new_url, headers=self.headers)

        try:
            response.raise_for_status()  # raise HTTP errors
        except Exception as err:
            print(err)
            return response

        json1 = response.json()['featureOfInterest']

        lst1 = [foi_parse(j) for j in json1 if isinstance(j, dict)]
        df1 = pd.DataFrame(lst1)

        ## bbox select
        if isinstance(bbox, list):
            df1 = df1[(df1.lon >= bbox[0][0]) & (df1.lat >= bbox[0][1]) & (df1.lon <= bbox[1][0]) & (df1.lat <= bbox[1][1])].copy()

        return df1


    def get_observation(self, foi, observed_property, procedure=None, from_date=None, to_date=None, retries=5):
        """

        """
        ### Chunk up the requests for the sake of the source server
        da1 = self.data_availability.copy()
        da1 = da1[(da1.featureOfInterest == foi) & (da1.observedProperty == observed_property)].iloc[0]

        if isinstance(from_date, str):
            from_date1 = pd.Timestamp(from_date)
        else:
            from_date1 = da1.fromDate.tz_localize(None)
        if isinstance(to_date, str):
            to_date1 = pd.Timestamp(to_date)
        else:
            to_date1 = da1.toDate.tz_localize(None)

        if (to_date1 - from_date1).days < (366*24):
            dr2 = [str(from_date1), str(to_date1)]
        else:
            dr1 = pd.date_range(from_date1, to_date1, freq='60M')
            dr2 = [str(d) for d in dr1]
            dr2[0] = str(from_date1)
            dr2[-1] = str(to_date1)

        ### Iterate through each date range
        self.request = 'GetObservation'

        df_list = []
        for i, d in enumerate(dr2[:-1]):
            print(d)
            from1 = d
            to1 = dr2[i+1]

            body = self.filters(foi, procedure, observed_property, from1, to1)
            body.update({'request': 'GetObservation'})

            new_url = self._url_convert(body)

            counter = retries
            while counter > 0:
                try:
                    response = requests.get(new_url, headers=self.headers, timeout=150)
                    break
                except:
                    print('Failed to extract data...trying again in 20 seconds...')
                    counter = counter - 1
                    sleep(20)
                    if counter == 0:
                        raise ValueError('Too many retries..something is wrong with the request.')

            response.raise_for_status()  # raise HTTP errors

            json1 = response.json()['observations']

            if json1:
                df1 = obs_process(json1)
                df_list.append(df1)

        if df_list:
            big_df1 = pd.concat(df_list)
            if 'phenomenonTime' in big_df1:
                big_df = big_df1.drop_duplicates('phenomenonTime')
            else:
                big_df = big_df1.drop_duplicates('resultTime')
        else:
            big_df = pd.DataFrame()

        return big_df

