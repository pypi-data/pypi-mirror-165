#!/usr/bin/env python3

#
# NOSA HEADER START
#
# The contents of this file are subject to the terms of the NASA Open
# Source Agreement (NOSA), Version 1.3 only (the "Agreement").  You may
# not use this file except in compliance with the Agreement.
#
# You can obtain a copy of the agreement at
#   docs/NASA_Open_Source_Agreement_1.3.txt
# or
#   https://sscweb.gsfc.nasa.gov/WebServices/NASA_Open_Source_Agreement_1.3.txt.
#
# See the Agreement for the specific language governing permissions
# and limitations under the Agreement.
#
# When distributing Covered Code, include this NOSA HEADER in each
# file and include the Agreement file at
# docs/NASA_Open_Source_Agreement_1.3.txt.  If applicable, add the
# following below this NOSA HEADER, with the fields enclosed by
# brackets "[]" replaced with your own identifying information:
# Portions Copyright [yyyy] [name of copyright owner]
#
# NOSA HEADER END
#
# Copyright (c) 2013-2021 United States Government as represented by
# the National Aeronautics and Space Administration. No copyright is
# claimed in the United States under Title 17, U.S.Code. All Other
# Rights Reserved.
#

"""
Module for accessing the Satellite Situation Center (SSC) web services
https://sscweb.gsfc.nasa.gov/WebServices/REST/.
"""

import platform
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError
import time
import logging
from typing import Dict, List, Tuple, Union
import requests
import dateutil.parser

from sscws import __version__, RETRY_LIMIT, ET_NS, ET_XHTML_NS
from sscws.coordinates import CoordinateSystem, CoordinateComponent
from sscws.outputoptions import CoordinateOptions, OutputOptions
from sscws.request import DataRequest, QueryRequest, SatelliteSpecification
from sscws.result import Result
from sscws.timeinterval import TimeInterval

#try:
#    import spacepy.datamodel as spdm    # type: ignore
#    SPDM_AVAILABLE = True
#except ImportError:
#    SPDM_AVAILABLE = False


class SscWs:
    """
    Class representing the web service interface to NASA's
    Satelite Situation Center (SSC) <https://sscweb.gsfc.nasa.gov/>.

    Parameters
    ----------
    endpoint
        URL of the SSC web service.  If None, the default is
        'https://sscweb.gsfc.nasa.gov/WS/sscr/2/'.
    timeout
        Number of seconds to wait for a response from the server.
    proxy
        HTTP proxy information.  For example,<pre>
        proxies = {
          'http': 'http://10.10.1.10:3128',
          'https': 'http://10.10.1.10:1080',
        }</pre>
        Proxy information can also be set with environment variables.
        For example,<pre>
        $ export HTTP_PROXY="http://10.10.1.10:3128"
        $ export HTTPS_PROXY="http://10.10.1.10:1080"</pre>
    ca_certs
        Path to certificate authority (CA) certificates that will
        override the default bundle.
    disable_ssl_certificate_validation
        Flag indicating whether to validate the SSL certificate.
    user_agent
        A value that is appended to the HTTP User-Agent values.

    Notes
    -----
    The logger used by this class has the class' name (SscWs).  By default,
    it is configured with a NullHandler.  Users of this class may configure
    the logger to aid in diagnosing problems.

    This class is dependent upon xml.etree.ElementTree module which is
    vulnerable to an "exponential entity expansion" and "quadratic blowup
    entity expansion" XML attack.  However, this class only receives XML
    from the (trusted) SSC server so these attacks are not a threat.  See
    the xml.etree.ElementTree "XML vulnerabilities" documentation for
    more details
    <https://docs.python.org/3/library/xml.html#xml-vulnerabilities>.
    """
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-arguments
    def __init__(
            self,
            endpoint=None,
            timeout=None,
            proxy=None,
            ca_certs=None,
            disable_ssl_certificate_validation=False,
            user_agent=None):

        self.logger = logging.getLogger(type(self).__name__)
        self.logger.addHandler(logging.NullHandler())

        self.retry_after_time = None

        self.logger.debug('endpoint = %s', endpoint)
        self.logger.debug('ca_certs = %s', ca_certs)
        self.logger.debug('disable_ssl_certificate_validation = %s',
                          disable_ssl_certificate_validation)

        if endpoint is None:
            self._endpoint = 'https://sscweb.gsfc.nasa.gov/WS/sscr/2/'
        else:
            self._endpoint = endpoint

        self._user_agent = 'sscws/' + __version__ + ' (' + \
            platform.python_implementation() + ' ' \
            + platform.python_version() + '; '+ platform.platform() + ')'

        if user_agent is not None:
            self._user_agent += ' (' + user_agent + ')'

        self._request_headers = {
            'Content-Type' : 'application/xml',
            'Accept' : 'application/xml',
            'User-Agent' : self._user_agent
        }
        self._session = requests.Session()
        #self._session.max_redirects = 0
        self._session.headers.update(self._request_headers)

        if ca_certs is not None:
            self._session.verify = ca_certs

        if disable_ssl_certificate_validation is True:
            self._session.verify = False

        if proxy is not None:
            self._proxy = proxy

        self._timeout = timeout

    # pylint: enable=too-many-arguments


    def __str__(self) -> str:
        """
        Produces a string representation of this object.

        Returns
        -------
        str
            A string representation of this object.
        """
        return 'SscWs(endpoint=' + self._endpoint + ', timeout=' + \
               str(self._timeout) + ')'


    def __del__(self):
        """
        Destructor.  Closes all network connections.
        """

        self.close()


    def close(self) -> None:
        """
        Closes any persistent network connections.  Generally, deleting
        this object is sufficient and calling this method is unnecessary.
        """
        self._session.close()


    def get_observatories(
            self
        ) -> Dict:
        """
        Gets a description of the available SSC observatories.

        Returns
        -------
        Dict
            Dictionary whose structure mirrors ObservatoryResponse from
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>
            with the addition of the following key/values:<br>
            - HttpStatus: with the value of the HTTP status code.
              Successful == 200.<br>
            When HttpStatus != 200:<br>
            - HttpText: containing a string representation of the HTTP
              entity body.<br>
            When HttpText is a standard SSC WS error entity body the
            following key/values (convenience to avoid parsing
            HttpStatus):<br>
            - ErrorMessage: value from HttpText.<br>
            - ErrorDescription: value from HttpText.<br>
        """
        url = self._endpoint + 'observatories'

        self.logger.debug('request url = %s', url)

        response = self._session.get(url, timeout=self._timeout)

        status = self.__get_status(response)
        if response.status_code != 200:
            return status

        observatory_response = ET.fromstring(response.text)

        result = {
            'Observatory': []
        }

        for observatory in observatory_response.findall(ET_NS + 'Observatory'):

            result['Observatory'].append({
                'Id': observatory.find(ET_NS + 'Id').text,
                'Name': observatory.find(ET_NS + 'Name').text,
                'Resolution': int(observatory.find(ET_NS + 'Resolution').text),
                'StartTime': dateutil.parser.parse(observatory.find(\
                    ET_NS + 'StartTime').text),
                'EndTime': dateutil.parser.parse(observatory.find(\
                    ET_NS + 'EndTime').text),
                'ResourceId': observatory.find(ET_NS + 'ResourceId').text
            })

        result.update(status)
        return result


    def get_ground_stations(
            self
        ) -> Dict:
        """
        Gets a description of the available SSC ground stations.

        Returns
        -------
        Dict
            Dictionary whose structure mirrors GroundStationResponse from
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>
            with the addition of the following key/values:<br>
            - HttpStatus: with the value of the HTTP status code.
              Successful == 200.<br>
            When HttpStatus != 200:<br>
            - HttpText: containing a string representation of the HTTP
              entity body.<br>
            When HttpText is a standard SSC WS error entity body the
            following key/values (convenience to avoid parsing
            HttpStatus):<br>
            - ErrorMessage: value from HttpText.<br>
            - ErrorDescription: value from HttpText.<br>
        """
        url = self._endpoint + 'groundStations'

        self.logger.debug('request url = %s', url)

        response = self._session.get(url, timeout=self._timeout)

        status = self.__get_status(response)
        if response.status_code != 200:
            return status

        ground_station_response = ET.fromstring(response.text)

        result = {
            'GroundStation': []
        }

        for ground_station in ground_station_response.findall(\
                ET_NS + 'GroundStation'):

            location = ground_station.find(ET_NS + 'Location')
            latitude = float(location.find(ET_NS + 'Latitude').text)
            longitude = float(location.find(ET_NS + 'Longitude').text)

            result['GroundStation'].append({
                'Id': ground_station.find(ET_NS + 'Id').text,
                'Name': ground_station.find(ET_NS + 'Name').text,
                'Location': {
                    'Latitude': latitude,
                    'Longitude': longitude
                }
            })

        result.update(status)
        return result


    def get_locations(
            self,
            param1: Union[List[str], DataRequest],
            time_range: Union[List[str], TimeInterval] = None,
            coords: List[CoordinateSystem] = None
        ) -> Dict:
        """
        Gets the specified locations.  Complex requests (requesting
        magnetic field model values) require a single DataRequest
        parameter.  Simple requests (for only x, y, z, lat, lon,
        local_time) require at least the first two paramters.

        Parameters
        ----------
        param1
            A locations DataRequest or a list of observatory identifier
            (returned by get_observatories).
        time_range
            A TimeInterval or two element array of ISO 8601 string
            values of the start and stop time of requested data.  The
            datetime values should have a UTC timezone.  If the values
            have no timezone, it will be set to UTC.  A datetime with
            a non-UTC timezone, will have its value adjusted to UTC and 
            the returned data may not have the expected range.
        coords
            Array of CoordinateSystem values that location information
            is to be in.  If None, default is CoordinateSystem.GSE.
        Returns
        -------
        Dict
            Dictionary whose structure mirrors Result from
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>
            with the addition of the following key/values:<br>
            - HttpStatus: with the value of the HTTP status code.
              Successful == 200.<br>
            When HttpStatus != 200:<br>
            - HttpText: containing a string representation of the HTTP
              entity body.<br>
            When HttpText is a standard SSC WS error entity body the
            following key/values (convenience to avoid parsing 
            HttpStatus):<br>
            - ErrorMessage: value from HttpText.<br>
            - ErrorDescription: value from HttpText.<br>
        Raises
        ------
        ValueError
            If param1 is not a DataRequest and time_range is missing or
            time_range does not contain valid values.
        """

        if isinstance(param1, DataRequest):
            request = param1
        else:
            request = SscWs.__create_locations_request(param1, time_range,
                                                       coords)

        return self.__get_locations(request)


    #def get_data_from_files(
    #        self,
    #        files: FileResult
    #    ) -> List['spdm.SpaceData']:
    #    """
    #    Gets the given files from the server and returns the contents
    #    in a SpaceData objects.
    #
    #    Parameters
    #    ----------
    #    files
    #        requested files.
    #    Returns
    #    -------
    #    List[SpaceData] ???
    #        The contents of the given files in a SpaceData objects.
    #    """
    #    import spacepy.datamodel as spdm        # type: ignore


    @staticmethod
    def __create_locations_request(
            obs_ids: List[str],
            time_range: Union[List[str], TimeInterval] = None,
            coords: List[CoordinateSystem] = None
        ) -> DataRequest:
        """
        Creates a "simple" (only x, y, z, lat, lon, local_time in GSE)
        locations DataRequest for the given values.
        More complicated requests should be made with DataRequest
        directly.

        Parameters
        ----------
        obs_ids
            A list of observatory identifier (returned by
            get_observatories).
        time_range
            A TimeInterval or two element array of ISO 8601 string
            values of the start and stop time of requested data.
        coords
            Array of CoordinateSystem values that location information
            is to be in.  If None, default is CoordinateSystem.GSE.
        Returns
        -------
        DataRequest
            A simple locations DataRequest based upon the given values.
        Raises
        ------
        ValueError
            If time_range is missing or time_range does not contain
            valid values.
        """

        sats = []
        for sat in obs_ids:
            sats.append(SatelliteSpecification(sat, 1))

        if time_range is None:
            raise ValueError('time_range value is required when ' +
                             '1st is not a DataRequest')

        if isinstance(time_range, list):
            time_interval = TimeInterval(time_range[0], time_range[1])
        else:
            time_interval = time_range

        if coords is None:
            coords = [CoordinateSystem.GSE]

        coord_options = []
        for coord in coords:
            coord_options.append(
                CoordinateOptions(coord, CoordinateComponent.X))
            coord_options.append(
                CoordinateOptions(coord, CoordinateComponent.Y))
            coord_options.append(
                CoordinateOptions(coord, CoordinateComponent.Z))
            coord_options.append(
                CoordinateOptions(coord, CoordinateComponent.LAT))
            coord_options.append(
                CoordinateOptions(coord, CoordinateComponent.LON))
            coord_options.append(
                CoordinateOptions(coord, CoordinateComponent.LOCAL_TIME))

        return DataRequest(None, time_interval, sats, None,
                           OutputOptions(coord_options), None, None)


    def __get_locations(
            self,
            request: DataRequest
        ) -> Dict:
        """
        Gets the given locations DataRequest.

        Parameters
        ----------
        request
            A locations DataRequest.
        Returns
        -------
        Dict
            Dictionary whose structure mirrors Result from
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>
            with the addition of the following key/values:<br>
            - HttpStatus: with the value of the HTTP status code.
              Successful == 200.<br>
            When HttpStatus != 200:<br>
            - HttpText: containing a string representation of the HTTP
              entity body.<br>
            When HttpText is a standard SSC WS error entity body the
            following key/values (convenience to avoid parsing 
            HttpStatus):<br>
            - ErrorMessage: value from HttpText.<br>
            - ErrorDescription: value from HttpText.<br>
        """
        url = self._endpoint + 'locations'

        self.logger.debug('__get_locations: POST request url = %s', url)

        xml_data_request = request.xml_element()

        #self.logger.debug('request XML = %s',
        #                  ET.tostring(xml_data_request))

        for retries in range(RETRY_LIMIT):

            response = self._session.post(url,
                                          data=ET.tostring(xml_data_request),
                                          timeout=self._timeout)
            if response.status_code == 429 or \
               response.status_code == 503 and \
               'Retry-After' in response.headers:

                retry_after = response.headers['Retry-After']

                self.logger.debug('429/503 status with Retry-After header: %s',
                                  retry_after)
                retry_after = int(retry_after)

                self.logger.info('Sleeping %d seconds before retrying request',
                                 retry_after)
                time.sleep(retry_after)
            else:
                break

        return self.__get_result(response)


    @staticmethod
    def __get_status(
            response: requests.Response
        ) -> Dict:
        """
        Gets status information from the given response.  In particular,
        when status_code != 200, an attempt is made to extract the SSC WS
        ErrorMessage and ErrorDescription from the response.

        Parameters
        ----------
        response
            requests Response object.

        Returns
        -------
        Dict
            Dict containing the following:<br>
            - HttpStatus: the HTTP status code<br>
            additionally, when HttpStatus != 200<br>
            - ErrorText: a string representation of the entire entity 
              body<br>
            - ErrorMessage: SSC WS ErrorMessage (when available)<br>
            - ErrorDescription: SSC WS ErrorDescription (when available)
        """
        http_result = {
            'HttpStatus': response.status_code
        }

        if response.status_code != 200:

            http_result['ErrorText'] = response.text
            try:
                error_element = ET.fromstring(response.text)
                http_result['ErrorMessage'] = error_element.findall(\
                    './/' + ET_XHTML_NS + 'p[@class="ErrorMessage"]/' +
                    ET_XHTML_NS + 'b')[0].tail
                http_result['ErrorDescription'] = error_element.findall(\
                    './/' + ET_XHTML_NS + 'p[@class="ErrorDescription"]/' +
                    ET_XHTML_NS + 'b')[0].tail
            except:
                pass  # ErrorText is the best we can do

        return http_result


    def __get_result(
            self,
            response: requests.Response
        ) -> Dict:
        """
        Creates a dict representation of a Result from the given response.

        Parameters
        ----------
        response
            A response from a web service request.

        Returns
        -------
        Dict
            Dict representation of a Result as described in
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>
            with the addition of an HttpStatus key with the value of the
            HTTP status code.  When HttpStatus != 200, a key named 
            HttpText will contain a string representation of the entity
            body.  And if the HttpText is a standard SSC WS error
            entity body, then keys named ErrorMessage and ErrorDescription
            will contain the values from the SSC WS error entity body
            (saving the caller the trouble of parsing HttpText).
        """

        status = self.__get_status(response)
        if response.status_code != 200:
            return status

        element = ET.fromstring(response.text)

        result_element = element.find(ET_NS + 'Result')

        if result_element is None:
            result_element = element.find(ET_NS + 'QueryResult')

        result = Result.get_result(result_element)
        result.update(status)
        return result


    def get_conjunctions(
            self,
            query: QueryRequest
        ) -> Dict:
        """
        Gets the conjunctions specified by query.

        Parameters
        ----------
        query
            Conjunction query request.
        Returns
        -------
        Dict
            Dictionary whose structure mirrors QueryResult from
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>
            with the addition of the following key/values:<br>
            - HttpStatus: with the value of the HTTP status code.
              Successful == 200.<br>
            When HttpStatus != 200:<br>
            - HttpText: containing a string representation of the HTTP
              entity body.<br>
            When HttpText is a standard SSC WS error entity body the
            following key/values (convenience to avoid parsing 
            HttpStatus):<br>
            - ErrorMessage: value from HttpText.<br>
            - ErrorDescription: value from HttpText.<br>
        Raises
        ------
        ValueError
            If query is invalid.
        """

        url = self._endpoint + 'conjunctions'

        self.logger.debug('POST request url = %s', url)

        xml_query_request = query.xml_element()

        self.logger.debug('request XML = %s',
                          ET.tostring(xml_query_request))

        for retries in range(RETRY_LIMIT):

            response = self._session.post(url,
                                          data=ET.tostring(xml_query_request),
                                          timeout=self._timeout)
            if response.status_code == 429 or \
               response.status_code == 503 and \
               'Retry-After' in response.headers:

                retry_after = response.headers['Retry-After']

                self.logger.debug('429/503 status with Retry-After header: %s',
                                  retry_after)
                retry_after = int(retry_after)

                self.logger.info('Sleeping %d seconds before retrying request',
                                 retry_after)
                time.sleep(retry_after)
            else:
                break

        status = self.__get_status(response)
        if response.status_code != 200:
            return status

        #self.logger.debug('response XML = %s', response.text)

        result = self.__get_result(response)
        result.update(status)
        return result


    @staticmethod
    def print_files_result(
            result: Dict):
        """
        Prints a Result containing files names document.

        Parameters
        ----------
        result
            Dict representation of Result as described
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
        """
        for file in result['Files']:
            print(file['Name'])


    @staticmethod
    def print_locations_result(
            result: Dict
        ) -> None:    # pylint: disable=too-many-branches
        """
        Prints a Dict representation of a Result.

        Parameters
        ----------
        result
            Dict representation of a Result as described
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
        """

        #print('StatusCode:', result['StatusCode'],
        #      'StatusSubCode:', result['StatusSubCode'])
        #print(result)

        if 'Files' in result:
            SscWs.print_files_result(result)
            return

        for data in result['Data']:
            if 'Coordinates' not in data:
                continue
            for coords in data['Coordinates']:
                print(data['Id'], coords['CoordinateSystem'].value)
                print('Time                     ', 'X                     ',
                      'Y                     ', 'Z                     ')
                for index in range(min(len(data['Time']), len(coords['X']))):
                    print(data['Time'][index], coords['X'][index],
                          coords['Y'][index], coords['Z'][index])

                if 'BTraceData' in data:
                    for b_trace in data['BTraceData']:

                        print(b_trace['CoordinateSystem'].value,
                              b_trace['Hemisphere'].value,
                              'Magnetic Field-Line Trace Footpoints')
                        print('Time                          ', 'Latitude        ',
                              'Longitude   ', 'Arc Length')
                        for index in range(min(len(data['Time']),
                                               len(b_trace['Latitude']))):
                            print(data['Time'][index],
                                  '{:15.5f} {:15.5f} {:15.5f}'.format(\
                                      b_trace['Latitude'][index],
                                      b_trace['Longitude'][index],
                                      b_trace['ArcLength'][index]))

                quantities = ['RadialLength', 'MagneticStrength',
                              'NeutralSheetDistance', 'BowShockDistance',
                              'MagnetoPauseDistance', 'DipoleLValue',
                              'DipoleInvariantLatitude', 'SpacecraftRegion',
                              'RadialTracedFootpointRegions',
                              'NorthBTracedFootpointRegions',
                              'SouthBTracedFootpointRegions']

                for quantity in quantities:
                    SscWs.print_time_series(quantity, data)

                if 'BGseX' in data and data['BGseX'] is not None:

                    min_len = min(len(data['Time']), len(data['BGseX']))
                    if min_len > 0:
                        print('{:25s} {:^30s}'.format('Time', 'B Strength GSE'))
                        print('{:25s} {:^9s} {:^9s} {:^9s}'.format('', 'X', 'Y', 'Z'))
                        for index in range(min_len):
                            print('{:25s} {:9.6f} {:9.6f} {:9.6f}'.format(\
                                  data['Time'][index].isoformat(),\
                                  data['BGseX'][index],\
                                  data['BGseY'][index],\
                                  data['BGseZ'][index]))

                if 'NorthBTracedFootpointRegion' in data and \
                   'SouthBTracedFootpointRegion' in data:

                    min_len = min(len(data['Time']),
                                  len(data['NorthBTracedFootpointRegion']))
                    if min_len > 0:
                        print('                 B-Traced Footpoint Region')
                        print('Time                     ', 'North            ',
                              'South           ')
                        for index in range(min_len):
                            print(data['Time'][index],
                                  data['NorthBTracedFootpointRegion'][index].value,
                                  data['SouthBTracedFootpointRegion'][index].value)


    @staticmethod
    def print_time_series(
            name: str,
            data: Dict
        ) -> None:
        """
        Prints the given time-series data.

        Parameters
        ----------
        name
            Name (key) of data to print.
        data
            Dict containing the values to print.
        """

        if name in data and data[name] is not None:
            min_len = min(len(data['Time']), len(data[name]))
            if min_len > 0:
                print('Time                     ', name)
                for index in range(min_len):
                    print(data['Time'][index], data[name][index])


    @staticmethod
    def print_conjunction_result(
            result: Dict
        ) -> None:
        """
        Prints the given Dict representation of a QueryResult.

        Parameters
        ----------
        result
            Dict representation of QueryResult as described
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
        """

        print('StatusCode:', result['StatusCode'],
              'StatusSubCode:', result['StatusSubCode'])
        #print(result)

        for conjunction in result['Conjunction']:
            print(conjunction['TimeInterval']['Start'].isoformat(), 'to',
                  conjunction['TimeInterval']['End'].isoformat())
            print('  {:10s} {:>7s} {:>7s} {:>9s} {:20s} {:>7s} {:>7s} {:>9s}'.format(\
                  'Satellite', 'Lat', 'Lon', 'Radius',
                  'Ground Station', 'Lat', 'Lon', 'ArcLen'))
            for sat in conjunction['SatelliteDescription']:
                for description in sat['Description']:
                    trace = description['TraceDescription']
                    print('  {:10s} {:7.2f} {:7.2f} {:9.2f} {:20s} {:7.2f} {:7.2f} {:9.2f}'.format(\
                          sat['Satellite'],
                          description['Location']['Latitude'],
                          description['Location']['Longitude'],
                          description['Location']['Radius'],
                          trace['Target']['GroundStation'],
                          trace['Location']['Latitude'],
                          trace['Location']['Longitude'],
                          trace['ArcLength']))
