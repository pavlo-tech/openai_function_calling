# openai_function_calling 

just messing around with openai function calling and modifying the openai example

you need the following API keys in your environment variables:
```
OPENAI_API_KEY 
TOMORROW_IO_API_KEY
```

References:
- [open ai api reference](https://platform.openai.com/docs/api-reference)

- [tomorrow io api reference (for weather data)](https://docs.tomorrow.io/reference/realtime-weather)


Example usage:
```
$ python3 main.py 
Ask AI a question (enter 'q' to quit): hello robot, I am travelling to New York. What is the weather like today?
AI: The current weather in New York is as follows:
- Temperature: 70.03 °F
- Cloud Cover: 61%
- Humidity: 60%
- Wind Speed: 6.99 mph
- Visibility: 9.94 miles

Please note that this information is subject to change.
Ask AI a question (enter 'q' to quit): is that colder than Austin, Texas right now?
AI: The current temperature in New York is 70.03°F, while in Austin, Texas it is 84.43°F. So it is colder in New York right now compared to Austin, Texas.
Ask AI a question (enter 'q' to quit): q
```