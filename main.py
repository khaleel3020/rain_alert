import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient
proxy_client = TwilioHttpClient()
proxy_client.session.proxies = {'https': os.environ['https_proxy']}

api_key = os.environ.get("api_key")
account_sid = 'ACf1a89f94435df65a63a0eb1dc7563516'
auth_token = os.environ.get("auth_token")
lat = 12.916517
long = 79.132500
parameter={
    "lat": lat,
    "lon": long,
    "appid": api_key,
    "exclude": "minutely,daily,current"
}
response = requests.get(url="https://api.openweathermap.org/data/2.5/onecall?", params=parameter)
response.raise_for_status()
weather_data = response.json()
slice_data = weather_data['hourly'][:12]
will_rain = False
for hour_data in slice_data:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True
if will_rain:
    print("Bring Umbrella")
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
        body="It's going to rain today. don't forget to take umbrella .",
        from_='19199269381',
        to='+918608916409'
    )
    print(message.status)