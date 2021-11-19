### Grafana-API

Grafana exposes an API that allows for CRUD operations to be done on dashboards present in a Grafana instance. Grafana itself does not provide an easy way to import a lot of dashboards through the user interface, which lead to the creation of Grafana-API. Grafana-API is a script that makes a GET request for all of the JSON models for our dashboards that are hosted on GitHub, and then creates or updates the dashboards on the targeted grafana server to the newest version available on GitHub.

#### Usage

By default, the script pulls data from the Async-Clock/Senior-Design repository. This can be changed to any URL you can make a GET request to, or can be made to target local JSON files. Line 61 must also be updated before use for the first time:

    api_response = requests.post('http://$basic-auth-here$@localhost:3000/api/dashboards/db/', data=json.dumps(r), headers=myheads)

The string 'http://\$basic-auth-here\$@localhost:3000/api/dashboards/db/' should be changed to target your Grafana server. Basic authentication is used for this script.

Example with Grafana default username and password:

    api_response = requests.post('http://admin:admin@localhost:3000/api/dashboards/db/', data=json.dumps(r), headers=myheads)

The script does not currently support using API keys.
