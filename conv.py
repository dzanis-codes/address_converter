import geopy
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim

from geopy.extra.rate_limiter import RateLimiter
#import sqlite3
import csv

locator = Nominatim(user_agent='none')
geocode = RateLimiter(locator.geocode, min_delay_seconds=1)


with open('rest_adreses.csv', encoding='utf-8-sig') as o:
    myData = csv.reader(o, quotechar='"') 
    for row in myData:
        #print(row)
        #search_term = []
        for element in row:
            #element vajag atbrivot no pedinjam
            print(len(element))
            print(element.find('LV-'))

            element = element.replace('"', '').strip()
            element = element.replace('pag.', 'pagasts').strip()
            element = element.replace('nov.', 'novads').strip()
            length_c = element.find('LV-')
            if length_c < 0:
                length_c = len(element)
            else:
                print("ok")
                
            element = element[:length_c]

            print(element)
   
        #print(search_term)
        location = locator.geocode(element) 
        if location == None:
            print("na")
            #sheit japamegina atrast izmetot ara pagastu un atstājot tikai novadu.
            len_pag = element.find(' pagasts')
            pag_nosaukums_start = element.rfind(' ', 0, len_pag)
            print(len_pag)
            print(pag_nosaukums_start)
            part1 = element[:pag_nosaukums_start]
            part2 = element[len_pag + 8:]
            new_el = part1 + part2
            print(new_el)
            location = locator.geocode(new_el) 
            print(location.latitude)
            print(location.longitude)
            print(location.raw['type'])
            print(location.raw['class'])
            #sheit jamegina novienadot shis divas lietas varbut vienaa funkcijaa

        else:
            #print('Latitude = {}, Longitude = {}'.format(location.latitude, location.longitude))
            print(location.latitude)
            print(location.longitude)
            print(location.raw['type'])
            print(location.raw['class'])

