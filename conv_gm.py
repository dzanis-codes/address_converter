import geopy
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import GoogleV3

from geopy.extra.rate_limiter import RateLimiter
import sqlite3
import csv

path1 = '/LBApp/adreses_for_gm.txt'
path2 = '/LBData/address_coords2.db'

conn = sqlite3.connect(path2) 
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS results
           (name_id INTEGER PRIMARY KEY, orig_address, search_term, latitude, longitude, type, class)''')
# Save (commit) the changes
conn.commit()


locator = GoogleV3(api_key=google_key)
geocode = RateLimiter(locator.geocode, min_delay_seconds=1)



with open(path1, encoding='utf-8-sig') as o:
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
            length_c = len(element) + 2
        else:
            print("ok")
        
        #naakošā rindiņa nogriež indeksu, jo openstreetmap tas nepatīk
        element = element[:length_c - 2]
        print(element)
   

        location = locator.geocode(element)
        print(location)
        print(location.raw)
        if location == None:
            print("na")
            len_pag = element.find(' pagasts')
            
            #ja nevar atrast dēļ pagasta tad šis
            if len_pag > 0:
                pag_nosaukums_start = element.rfind(' ', 0, len_pag)
                print(len_pag)
                print(pag_nosaukums_start)
                part1 = element[:pag_nosaukums_start]
                part2 = element[len_pag + 8:]
                element = part1 + part2
                print(element)
                location = locator.geocode(element)
                if location != None: 

                    print(location.latitude)
                    print(location.longitude)

                    latitude = location.latitude
                    longitude = location.longitude
                    a_type = 'na'
                    a_class = 'na'          
                    #sheit jamegina novienadot shis divas lietas varbut vienaa funkcijaa
                elif element.find(' novads') > 0:
                    print(element.find(' novads'))
                    nov_nosaukums_start = element.rfind(' ', 0, element.find(' novads'))
                    part1 = element[:pag_nosaukums_start]
                    part2 = element[len_pag + 7:]
                    element = part1 + part2
                    print(element)
                    location = locator.geocode(element)
                    if location != None: 
                        latitude = 'na'
                        longitude = 'na'
                        a_type = 'na'
                        a_class = 'na'   
                else:    
                    latitude = 'na'
                    longitude = 'na'
                    a_type = 'na'
                    a_class = 'na'              
            #ja nevar atrast dēļ korpusa tad šis
            elif element.find('k-') > 0:
                len_korpuss = element.find('k-')
                print(len_korpuss)
                part1 = element[:len_korpuss]
                part2 = element[len_korpuss + 3:]
                element = part1 + part2
                print(element)
                location = locator.geocode(element) 
                if location != None: 
                    print(location.latitude)
                    print(location.longitude)

                    latitude = location.latitude
                    longitude = location.longitude
                    a_type = 'na'
                    a_class = 'na'
            else:
                latitude = 'na'
                longitude = 'na'
                a_type = 'na'
                a_class = 'na'      
        else:
            print(location.latitude)
            print(location.longitude)
            print(location)
            print(location.raw)

            latitude = location.latitude
            longitude = location.longitude
            a_type = 'na'
            a_class = 'na'     
        
        sql_entry = (str(original_a), str(element), str(latitude), str(longitude), str(a_type), str(a_class)) 
        c.execute("INSERT INTO results VALUES (null, ?, ?, ?, ?, ?, ?)", sql_entry)
        
        conn.commit()
