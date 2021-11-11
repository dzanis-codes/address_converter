import geopy
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import GoogleV3

from geopy.extra.rate_limiter import RateLimiter
import sqlite3
import csv

path1 = '/LBApp/jur_adres_conv.csv'
path2 = '/LBData/address_coords4.db'


conn = sqlite3.connect(path2) 
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS results
           (name_id INTEGER PRIMARY KEY, orig_address, search_term, latitude, longitude, type, class)''')
# Save (commit) the changes
conn.commit()


locator = Nominatim(user_agent='none')
geocode = RateLimiter(locator.geocode, min_delay_seconds=1)



with open(path1, encoding='utf-8-sig') as o:
    myData = csv.reader(o, quotechar='"') 
    for row in myData:
        print(row)
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
        
 
        element = element[:length_c - 2]
        print(element)
   

        location = locator.geocode(element) 
        if location == None:
            print("pilno adresi neatrada")
            len_pag = element.find(' pagasts')
            print("pagasts:" + str(len_pag))
        
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
                    a_type = location.raw['type']
                    a_class = location.raw['class']            
                    #sheit jamegina novienadot shis divas lietas varbut vienaa funkcijaa
                else:    
                    latitude = 'na'
                    longitude = 'na'
                    a_type = 'na'
                    a_class = 'na'              
            #ja nevar atrast dÄ“Ä¼ korpusa tad Åis
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
                    a_type = location.raw['type']
                    a_class = location.raw['class']
            else:
                latitude = 'na'
                longitude = 'na'
                a_type = 'na'
                a_class = 'na'      
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
        latitude = 'na'
        longitude = 'na'
