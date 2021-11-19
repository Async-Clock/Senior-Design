# Grafana-Pull

Grafana-pull is a tool designed to make backing up grafana dashboards a simple, automated process. The script is configured to target a grafana server running on the local machine, with a default username and password. 

## Usage

To use the script, insure python is installed along with the requests library, then run the script. **The script will create a new JSON file for each dashboard in the directory the script is ran in.** 

## Notes

The script makes slight changes to the JSON models recieved from the Grafana API.

    #Cleans up the junk from the response objects and gets the JSON ready for use
    for x in dash_json:
        x['dashboard']['id'] = None
        x['dashboard']['version'] = None
        x['overwrite'] = True
        del x['meta']

This is done to make the JSON useable by [Grafana-api](https://github.com/Async-Clock/Senior-Design/tree/main/Scripts/Grafana-API). Having an incorrect 'version' or 'id' field can lead to the API refusing to update or create dashboards. See the [Grafana JSON model documentation](https://grafana.com/docs/grafana/latest/dashboards/json-model/) for more information.
