"""
Geocodes HPD corporate owner addresses using the NYC geoclient API
Copyright (C) 2016 Ziggy Mintz

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from nyc_geosearch import Geosearch
import os
import sys
import csv
import time
import json

GEOSEARCH_FILE = sys.argv[1]

g = Geosearch()

ERRORS = 0
PROCESSED = 0

def geosearch():
    with open(GEOSEARCH_FILE + '-geosearch.csv', 'a') as geocode_file:
        writer = csv.writer(geocode_file, delimiter=",")
        with open(GEOSEARCH_FILE, 'r') as f:
            # csv_file = csv.DictReader(f, delimiter=",")
            csv_file = csv.reader(f, delimiter=",")


            headers = next(csv_file, None)  # skip the headers
            writer.writerow(headers + [u'bbl_alt', u'lng_alt', u'lat_alt'])

            for row in csv_file:
                # address = row['cleaned_address']
                address = row[12]
                # print(address)
                info = g.address(address)['features'][0]
                try:
                    bbl_alt = info['properties']['pad_bbl']
                    lng_alt = info['geometry']['coordinates'][0]
                    lat_alt = info['geometry']['coordinates'][1]
                    # xcoord = info['xCoordinate']
                    # ycoord = info['yCoordinate']
                    # council_district = info['cityCouncilDistrict']
                    # community_district = info['communityDistrict']
                    # print(bbl_alt)
                    # writer.writerow(list(row.items()) + [bbl_alt, lng_alt, lat_alt])
                    writer.writerow(row + [bbl_alt, lng_alt, lat_alt])
                except KeyError as e:
                    global ERRORS
                    ERRORS += 1
                    try:
                        print("error: " + str(house_number) + " " + str(street) + " - " + info['message'])
                    except KeyError as e:
                        print('A key error occurred with this dictionary:')
                        print(info)
                finally:
                    global PROCESSED
                    PROCESSED += 1
                    if PROCESSED % 25 == 0:
                        time.sleep(5)

try:
    geosearch()
    # value = g.address('hi dan')
    # print(json.dumps(value, indent=4))
    print("A total of " + str(PROCESSED) + " addresses were processed.")
    print("there were " + str(ERRORS) + " addresses that did not geocode")
except Exception:
    print('something went wrong with ' + GEOSEARCH_FILE)
    raise
