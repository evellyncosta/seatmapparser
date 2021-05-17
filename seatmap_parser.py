import xml.etree.ElementTree as ET
from copy import deepcopy
import json
import sys

def get_column_postion(column, columns_definitions):
    for column_definition in columns_definitions:
        position_name = column_definition.get('Position') 
        if(column==position_name):
            return column_definition.text

def get_prices(seat_offer_id, la_carte_offer_list):
    for offer in la_carte_offer_list:
        offer_id = offer.get('OfferItemID') 

        if(seat_offer_id==offer_id):
            for simple_currency_price in offer.findall('.//{http://www.iata.org/IATA/EDIST/2017.2}SimpleCurrencyPrice'):
                fees = {
                    'price': simple_currency_price.text,
                    'currency': simple_currency_price.get('Code') ,
                }
                
                return fees

def get_seat_definition(seat_definition_id, seat_definition_list):

    for seat_definition in seat_definition_list:
        definition_id = seat_definition.get('SeatDefinitionID') 
        
        if(seat_definition_id==definition_id): 
            description = seat_definition.find('.//{http://www.iata.org/IATA/EDIST/2017.2}Text')
            return description.text

filename = sys.argv[-1]

tree = ET.parse(filename)

root = tree.getroot()

alist = []

iata_address = '{http://www.iata.org/IATA/EDIST/2017.2}SeatAvailabilityRS'

open_travel_address = '{http://schemas.xmlsoap.org/soap/envelope/}Envelope'


if(root.tag == iata_address):    
    offer_list = root.findall('.//{http://www.iata.org/IATA/EDIST/2017.2}ALaCarteOfferItem')
    service_definition_list = root.findall('.//{http://www.iata.org/IATA/EDIST/2017.2}SeatDefinition')

    for cabinLayout in root.findall('.//{http://www.iata.org/IATA/EDIST/2017.2}CabinLayout'):

        column_postions = cabinLayout.findall('.//{http://www.iata.org/IATA/EDIST/2017.2}Columns')

        

        for row in root.findall('.//{http://www.iata.org/IATA/EDIST/2017.2}Row'):
            seat_offer_id = row.find('.//{http://www.iata.org/IATA/EDIST/2017.2}OfferItemRefs')
            

            if(seat_offer_id != None):
                    seat_offer_id = seat_offer_id.text
                    price = get_prices(seat_offer_id, offer_list)
                     
    
            for row_number in row.findall('.//{http://www.iata.org/IATA/EDIST/2017.2}Number'):
                row_number = row_number.text
            
        
            for seat_list in row.findall('.//{http://www.iata.org/IATA/EDIST/2017.2}Seat'):
                seat_column_uncoverted = seat_list.find('.//{http://www.iata.org/IATA/EDIST/2017.2}Column').text            
                seat_type = get_column_postion(seat_column_uncoverted,column_postions)
                
                for seat in seat_list.findall('.//{http://www.iata.org/IATA/EDIST/2017.2}SeatDefinitionRef'):
                    seat_definition_ref = seat.text
                    description = get_seat_definition(seat_definition_ref, service_definition_list) 
                                 

                    row_info = {
                        'row_number': row_number,
                        'seat_definition_ref': seat_definition_ref,
                        'column': seat_column_uncoverted,
                        'description': description
                    }

                    if(seat_type != None):
                        row_info['seat_type'] = seat_type

                    if(seat_offer_id != None):
                        row_info['fees'] = price


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



