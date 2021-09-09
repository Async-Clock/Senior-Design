import requests

# Links to JSON dashboard models contained within the github repository
target_urls = ["https://raw.githubusercontent.com/Async-Clock/Senior-Design/main/Dashboards/server-racks.json",
               "https://raw.githubusercontent.com/Async-Clock/Senior-Design/main/Dashboards/siu-campus.json",
               "https://raw.githubusercontent.com/Async-Clock/Senior-Design/main/Dashboards/siu-engr-e-2f.json",
               "https://raw.githubusercontent.com/Async-Clock/Senior-Design/main/Dashboards/siu-engrbuilding.json",
               "https://raw.githubusercontent.com/Async-Clock/Senior-Design/main/Dashboards/siu-morrislibrary.json",
               "https://raw.githubusercontent.com/Async-Clock/Senior-Design/main/Dashboards/siu-powerplant.json",
               "https://raw.githubusercontent.com/Async-Clock/Senior-Design/main/Dashboards/siu-rec.json"]

# Headers used for posting via the Grafana API
myheads = {'Accept' : 'application/json', 'Authorization' : 'Bearer $API_KEY', 'Content-Type' : 'application/json; charset=UTF-8'}

for x in target_urls:
    
    r = requests.get(x)
    # If the file was aquired successfully, pass the JSON model to the Grafana API
    if r.status_code == 200:
        api_response = requests.post('http://localhost:3000/api/dashboards/db/', data=r.text, headers=myheads)
        if api_response.status_code != 200:
            print("Issue with posting ", x)
            print(api_response.text)
    # Otherwise print out debug information
    else:
        print("Problem with ", end='')
        print(x)
        print(r)
        print(r.status_code)

print("-------------------------------------")
print("Dashboards Created/Updated")
print("-------------------------------------")