import xml.etree.ElementTree as ET
from copy import deepcopy
import json
import sys

filename = sys.argv[-1]

tree = ET.parse(filename)

root = tree.getroot()

alist = []

for row_info in root.findall('.//{http://www.opentravel.org/OTA/2003/05/common/}RowInfo'):
    seat_info = row_info.find('.//{http://www.opentravel.org/OTA/2003/05/common/}SeatInfo')
       
    summary = seat_info.find('.//{http://www.opentravel.org/OTA/2003/05/common/}Summary')
    
    cabin_type = row_info.get('CabinType')

    for seat_info in row_info.findall('.//{http://www.opentravel.org/OTA/2003/05/common/}SeatInfo'):
        summary = seat_info.find('.//{http://www.opentravel.org/OTA/2003/05/common/}Summary')
        available_ind = summary.get('AvailableInd')
        occupied_ind= summary.get('OccupiedInd')
        seat_number= summary.get('SeatNumber')
 
        features = seat_info.find('.//{http://www.opentravel.org/OTA/2003/05/common/}Features').text

        fee = seat_info.find('.//{http://www.opentravel.org/OTA/2003/05/common/}Fee')
        if fee != None:
            amount = fee.get('Amount')


    row_info = {
        'cabin_type': cabin_type,
        'available_ind': available_ind,
        'occupied_ind': occupied_ind,
        'seat_number': seat_number,
        'features': features,
    }


    dictionary_copy = row_info.copy()

    alist.append(dictionary_copy)

file = json.dumps(alist, indent=4)

with open('data.json', 'w') as f:
    json.dump(alist, f)
