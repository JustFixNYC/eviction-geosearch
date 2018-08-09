# -*- coding: utf-8 -*-

"""

"""

import requests

# from urllib import urlencode
import urllib.parse

class Geosearch(object):
    """
    This object's methods provide access to the NYC GeoSearch REST API.

    All methods return a dict, whether or not the geocoding succeeded.  If it
    failed, the dict will have a `message` key with information on why it
    failed.

    :param app_id:
        Your NYC Geoclient application ID.
    :param app_key:
        Your NYC Geoclient application key.
    """

    BASE_URL = u'https://geosearch.planninglabs.nyc/v1/search'

    def _request(self, **kwargs):
        kwargs.update({
            'size': '1'
        })

        # Ensure no 'None' values are sent to server
        for k in kwargs.keys():
            if kwargs[k] is None:
                kwargs.pop(k)

        return requests.get(u'{0}?{1}'.format(Geosearch.BASE_URL, urllib.parse.urlencode(kwargs))).json()

    def address(self, address):
        """
        Given a valid address, provides blockface-level, property-level, and
        political information.

        :param houseNumber:
            The house number to look up.
        :param street:
            The name of the street to look up.
        :param borough:
            The borough to look within.  Must be 'Bronx', 'Brooklyn',
            'Manhattan', 'Queens', or 'Staten Island' (case-insensitive).

        :returns: A dict with blockface-level, property-level, and political
            information.
        """
        return self._request(text=address)
