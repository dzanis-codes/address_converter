import geopy
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim

from geopy.extra.rate_limiter import RateLimiter
import sqlite3
import csv

path = 'address_coords.db'
conn = sqlite3.connect(path) 
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS results
           (name_id INTEGER PRIMARY KEY, orig_address, search_term, latitude, longitude, type, class)''')
# Save (commit) the changes
conn.commit()



locator = Nominatim(user_agent='none')
geocode = RateLimiter(locator.geocode, min_delay_seconds=1)





with open('rest_adreses.csv', encoding='utf-8-sig') as o:
    myData = csv.reader(o, quotechar='"') 
    for row in myData:
        #print(row)
        #search_term = []
        original_a = row[0]
        element = row[0]
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
   

        location = locator.geocode(element) 
        if location == None:
            print("na")
            len_pag = element.find(' pagasts')
            pag_nosaukums_start = element.rfind(' ', 0, len_pag)
            print(len_pag)
            print(pag_nosaukums_start)
            part1 = element[:pag_nosaukums_start]
            part2 = element[len_pag + 8:]
            element = part1 + part2
            print(element)
            location = locator.geocode(element) 
            print(location.latitude)
            print(location.longitude)

            latitude = location.latitude
            longitude = location.longitude
            a_type = location.raw['type']
            a_class = location.raw['class']            
            #sheit jamegina novienadot shis divas lietas varbut vienaa funkcijaa

        else:
            print(location.latitude)
            print(location.longitude)

            latitude = location.latitude
            longitude = location.longitude
            a_type = location.raw['type']
            a_class = location.raw['class']     
        
        sql_entry = (str(original_a), str(element), str(latitude), str(longitude), str(a_type), str(a_class)) 
        c.execute("INSERT INTO results VALUES (null, ?, ?, ?, ?, ?, ?)", sql_entry)
        
        conn.commit()
