import datetime
from zoneinfo import ZoneInfo

from google.adk.agents.llm_agent import Agent


def get_weather(city: str) -> dict:
    """Return the current weather in the specified city.
    Args:
          city (str): The name of the city to get the weather for.
     Returns:
             dict: A dictionary containing the weather information.
     """
    if city.lower() == "new york":
        return {
            "status": "success",
            "report": "The weather in New York is sunny with a high of 75°F."}
    else:
        return {
            "status": "error",
            "error_message": f"The weather data for {city} is not available."}


def get_current_time(city: str) -> dict:
    """Return the current time in the specified city.
    Args:
          city (str): The name of the city to get the current time for.
     Returns:
             dict: A dictionary containing the current time information.
     """
    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:
        return {
            "status": "error",
            "error_message": f"I don't have timezone information for {city}."
        }
    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now()
    report = f"The current time in {city} is {now.strftime('%Y-%m-%d %H:%M:%S')}"
    return {"status": "success", "report": report}

root_agent = Agent(
    model='gemini-2.5-flash',
    name='weather_time_agent',
    description='Agent to answer the weather and time in a city.',
    instruction='You are a helpful agent that can answer questions about the weather and time in a given city.',
    tools=[get_weather, get_current_time]
)
