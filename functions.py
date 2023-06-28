import json
import os
import requests

TOMORROW_IO_API_KEY = os.environ["TOMORROW_IO_API_KEY"]


# https://docs.tomorrow.io/reference/realtime-weather
def get_current_weather_for_location(args):
    lat, lon = float(args.get("latitude")), float(args.get("longitude"))
    key = TOMORROW_IO_API_KEY
    tomorrow_api_endpoint = "https://api.tomorrow.io/v4/weather/realtime"

    response_json = requests.get(
        f"{tomorrow_api_endpoint}?location={lat},{lon}&fields=temperature&units=imperial&apikey={key}"
    ).json()
    # print(response_json)
    return json.dumps(response_json)


get_current_weather_for_location_definition = {
    "name": "get_current_weather_for_location",
    "description": "get the current weather in a given location",
    "parameters": {
        "type": "object",
        "properties": {
            "latitude": {
                "type": "string",
                "description": "the latitude of the location to check the weather",
            },
            "longitude": {
                "type": "string",
                "description": "the longitude of the location to check the weather",
            },
        },
    },
}

functions = {
    "get_current_weather_for_location": {
        "method": get_current_weather_for_location,
        "definition": get_current_weather_for_location_definition,
    }
}
function_definitions = [v["definition"] for (k, v) in functions.items()]
