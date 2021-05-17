import xml.etree.ElementTree as ET
from copy import deepcopy
import json
import sys

def get_column_postion(column, columns_definitions):
    for column_definition in columns_definitions:
        position_name = column_definition.get('Position') 
        if(column==position_name):
            return column_definition.text

def get_service_definition(seat_definition_ref, service_definition_list):
    for service in service_definition_list:
        service_definition_id = service.get('ServiceDefinitionID') 
        print('###')
        print(service_definition_id)
        print('###ref')
        print(seat_definition_ref)
        if(seat_definition_ref==service_definition_id):
            print("equals")

filename = sys.argv[-1]

tree = ET.parse(filename)

root = tree.getroot()

alist = []

iata_address = '{http://www.iata.org/IATA/EDIST/2017.2}SeatAvailabilityRS'

open_travel_address = '{http://schemas.xmlsoap.org/soap/envelope/}Envelope'


if(root.tag == iata_address):
    service_destionation_list = root.findall('.//{http://www.iata.org/IATA/EDIST/2017.2}ServiceDefinition')    

    for cabinLayout in root.findall('.//{http://www.iata.org/IATA/EDIST/2017.2}CabinLayout'):

        column_postions = cabinLayout.findall('.//{http://www.iata.org/IATA/EDIST/2017.2}Columns')

        for row in root.findall('.//{http://www.iata.org/IATA/EDIST/2017.2}Row'):
    
            for row_number in row.findall('.//{http://www.iata.org/IATA/EDIST/2017.2}Number'):
                row_number = row_number.text
        
            for seat in row.findall('.//{http://www.iata.org/IATA/EDIST/2017.2}Seat'):
                seat_column_uncoverted = seat.find('.//{http://www.iata.org/IATA/EDIST/2017.2}Column').text            
                seat_type = get_column_postion(seat_column_uncoverted,column_postions)
                seat_definition_ref = seat.find('.//{http://www.iata.org/IATA/EDIST/2017.2}SeatDefinitionRef').text
            
  
            row_info = {
                'row_number': row_number,
                'seat_type': seat_type,
                'seat_definition_ref': seat_definition_ref
            }

            dictionary_copy = row_info.copy()

            alist.append(dictionary_copy)
    

if(root.tag == open_travel_address):
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



