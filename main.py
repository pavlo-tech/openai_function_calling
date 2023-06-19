import os
import openai
import requests
import json

from turn_enum import turn_enum

# https://docs.tomorrow.io/reference/realtime-weather

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
TOMORROW_IO_API_KEY = os.environ['TOMORROW_IO_API_KEY']
models = {
    'gpt3': 'gpt-3.5-turbo-0613',
    'gpt4': 'gpt-4-0613',
}


def get_current_weather_for_location(args):
    lat, lon = float(args.get('latitude')), float(args.get('longitude'))
    key = TOMORROW_IO_API_KEY
    tomorrow_api_endpoint = 'https://api.tomorrow.io/v4/weather/realtime'

    response_json = requests.get(
        f'{tomorrow_api_endpoint}?location={lat},{lon}&fields=temperature&units=imperial&apikey={key}'
    ).json()
    # print(response_json)
    return json.dumps(response_json)


functions = {
    'get_current_weather_for_location': {
        'method': get_current_weather_for_location,
        'definition': {
            'name': 'get_current_weather_for_location',
            'description': 'get the current weather in a given location',
            'parameters': {
                'type': 'object',
                'properties': {
                    'latitude': {
                        'type': 'string',
                        'description': 'the latitude of the location to check the weather'
                    },
                    'longitude': {
                        'type': 'string',
                        'description': 'the longitude of the location to check the weather'
                    },
                }
            },
        }
    }
}
function_definitions = [v['definition'] for (k, v) in functions.items()]


def process_turn_rec(messages: tuple, turn: turn_enum, function_call) -> None:
    if turn == turn_enum.USER:
        user_message = input('Ask AI a question (enter \'q\' to quit): ')
        if user_message == 'q':
            return
        else:
            return process_turn_rec(
                messages + ({
                                "role": "user",
                                "content": user_message
                            },),
                turn_enum.AI,
                None,
            )
    elif turn == turn_enum.AI:
        ai_message = openai.ChatCompletion.create(
            api_key=OPENAI_API_KEY,
            model=models['gpt3'],
            messages=messages,
            functions=function_definitions,
            function_call='auto',
        )["choices"][0]["message"]
        if ai_message.get('function_call'):
            return process_turn_rec(
                messages + (ai_message,),
                turn_enum.LOCAL_MACHINE,
                ai_message["function_call"]
            )
        else:
            print(f'AI: {ai_message.content}')
            return process_turn_rec(
                messages + (ai_message,),
                turn_enum.USER,
                None
            )
    elif turn == turn_enum.LOCAL_MACHINE:
        function_name = function_call['name']
        function_args = json.loads(function_call['arguments'])
        function_response = functions[function_name]['method'](function_args)
        function_message = {
            "role": "function",
            "name": function_name,
            "content": function_response,
        }
        print(f'local machine executed {function_name}')
        return process_turn_rec(
            messages + (function_message,),
            turn_enum.AI,
            None
        )


process_turn_rec((), turn_enum.USER, None)
