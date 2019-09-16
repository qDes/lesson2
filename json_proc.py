import json

with open('russia','r') as file_read:
    cities_str = file_read.read()

cities_json = json.loads(cities_str) 
cities_list = []
for elem in cities_json:
    cities_list.append(elem.get('city'))

with open("cities", 'wb') as file_write:
    file_write.write(json.dumps(cities_list).encode('utf-8'))

with open('cities','r') as f:
    cities = f.read()
print(json.loads(cities))

