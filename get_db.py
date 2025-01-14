import requests
apip = "192.168.1.163" 

def get_db(apip):
    try:
        tagsdb = []
        pos = 0
        busy = 1
        while busy==1:
            url = "http://{}/get_db?pos={}".format(apip, pos)

            response = requests.get(url)
            response.raise_for_status() 
            data = response.json()

            tags = data.get('tags', [])
            pos = data.get('continu', [])

            for entry in tags:
                mac = entry.get('mac')
                hw_type = entry.get('hwType')
                temperature = entry.get('temperature')
                battery = entry.get('batteryMv')
                if mac is not None and hw_type is not None:
                    tagsdb.append({'mac': mac, 'hwType': hw_type, 'Temp': temperature, 'Battery': battery})

            if pos == []:
                busy=0 # i guess we're done :)
    
    except requests.exceptions.RequestException as e:
        print("Error fetching data:", e)
    except ValueError as e:
        print("Error parsing JSON:", e)
    return tagsdb

tags = get_db(apip)

print(f"Number of tags in db: {len(tags)}")
print()

for item in tags:
    print(f"{item['mac']}, Type: {item['hwType']}, Temp {item['Temp']}, Batt {item['Battery']} mV")
