import requests
import json

# This function is for fixing JSON. Since we intend to pull the files from github, a
# consequence of this is the fact that there is a conflict between the JSON 'true'
# and Python 'True'. Usually python is able to automatically handle this, but since
# the files are pulled from github the boolean ends up being converted to a string,
# breaking the JSON. In paticular, the value for field "overwrite" must be of type
# boolean before it is converted by the built-in JSON library.

# The function works by recursively iterates through the entire JSON model passed in and 
# changes all booleans that have been converted into strings back into booleans

def fix_bool(json):
    mytype = type(json)
    if mytype == dict:
        for x in json:
            if type(json[x]) == list or type(json[x]) == dict:
                fix_bool(json[x])
            elif type(json[x]) == str:
                if json[x].lower() == 'true':
                    json[x] = True
                elif json[x].lower() == 'false':
                    json[x] = False
    elif mytype == list:
        for x in json:
            if type(x) == dict or type(x) == list:
                if type(x) == list or type(x) == dict:
                    fix_bool(x)
                elif type(x) == str:
                    if x.lower() == 'true':
                        x = True
                    elif x.lower() == 'false':
                        x = False
    else:
        print("error")
    return json


# Links to JSON dashboard models contained within the github repository
target_urls = ["https://raw.githubusercontent.com/Async-Clock/Senior-Design/main/Dashboards/server-racks.json",
               "https://raw.githubusercontent.com/Async-Clock/Senior-Design/main/Dashboards/siu-campus.json",
               "https://raw.githubusercontent.com/Async-Clock/Senior-Design/main/Dashboards/siu-engr-e-2f.json",
               "https://raw.githubusercontent.com/Async-Clock/Senior-Design/main/Dashboards/siu-engrbuilding.json",
               "https://raw.githubusercontent.com/Async-Clock/Senior-Design/main/Dashboards/siu-morrislibrary.json",
               "https://raw.githubusercontent.com/Async-Clock/Senior-Design/main/Dashboards/siu-powerplant.json",
               "https://raw.githubusercontent.com/Async-Clock/Senior-Design/main/Dashboards/siu-rec.json"]

# Headers used for posting via the Grafana API
myheads = {'Accept' : 'application/json', 'Content-Type' : 'application/json; charset=UTF-8'}

# Gets each of the JSON models that the links refer to, then calls
# fix_bool() to insure that the grafana API does not throw any 
# errors related to type mismatch
for x in target_urls:
    
    r = requests.get(x)
    # If the file was aquired successfully, pass the JSON model to the Grafana API
    if r.status_code == 200:
        r = fix_bool(r.json())
        api_response = requests.post('http://$basic-auth-here$@localhost:3000/api/dashboards/db/', data=json.dumps(r), headers=myheads)
        if api_response.status_code != 200:
            print("Issue with posting ", x)
            print(api_response.text)
            print(api_response.status_code)
    # Otherwise print out debug information
    else:
        print("Problem with ", end='')
        print(x)
        print(r)
        print(r.status_code)

print("-------------------------------------")
print("Dashboards Created/Updated")
print("-------------------------------------")
