# This python script is for pulling all the JSON models of all dashboards on a
# specific grafana instance. The JSON will be written to local files corresponding
# to the title of each dashboard listed in the JSON.
import requests
import json

grafana_link = 'http://admin:admin@localhost:3000/api/search?folderIds=0'

request_headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json; charset=UTF-8'}


#Step 1: Get list of dashboard uid's from the grafana API
temp = requests.get(grafana_link, headers=request_headers)

dash_json = temp.json()
dash_uid_list = []

for x in dash_json:
    dash_uid_list.append(x['uid'])

#Now pull all JSON using the uid's through the grafana API and add add the JSON to an empty list

dash_json = []
#Gets the JSON of all dashboards and adds it to the list dash_json
for x in dash_uid_list:
    grafana_link = 'http://admin:admin@localhost:3000/api/dashboards/uid/' + str(x)
    temp = requests.get(grafana_link, headers=request_headers)
    dash_json.append(temp.json())

#Cleans up the junk from the response objects and gets the JSON ready for use
for x in dash_json:
    x['dashboard']['id'] = None
    x['dashboard']['version'] = None
    x['overwrite'] = True
    del x['meta']

#Write the JSON to local files

for x in dash_json:
    file = open(x['dashboard']['title'] + '.json', 'w')
    file.write(json.dumps(x, indent=1))
    file.close()
print('Pull complete, ENTER to exit')
x = input()

