import requests
import json
import datetime
import openai

# Set OpenAI API key
openai.api_key = "2tVIlhDk964yyk17sm5TT3BlbkFJkYWiGlypwwB0F78n6rLa"

# KakaoTalk API URL and Access Token
url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
access_token = "nREu6jZeWw8KDN9xZ2nxtZX4mEk2umhk83FxPpUKCj1ylwAAAYeqzph8"

# KMA API URL and API key
weather_url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst"
api_key = "MnGOdrqbM1wstw7ArZGsMENbxjYa7BTcueKzvEq9fGn22H9OqprbGL1MhAbOtS6LBVShAAjpM/qAnsc5Ia9ntA=="

# Location information (latitude, longitude)
nx = "your_x_coordinate"
ny = "your_y_coordinate"

# Fine dust level API URL
dust_url = "http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty"

# Get current weather data
weather_response = requests.get(weather_url, params={
    "serviceKey": api_key,
    "numOfRows": 1,
    "pageNo": 1,
    "dataType": "JSON",
    "base_date": datetime.datetime.today().strftime("%Y%m%d"),
    "base_time": datetime.datetime.now().strftime("%H%M"),
    "nx": nx,
    "ny": ny
})
weather_data = json.loads(weather_response.text)

# Get fine dust level data
dust_response = requests.get(dust_url, params={
    "stationName": "your_station_name",
    "dataTerm": "DAILY",
    "ver": "1.0",
    "serviceKey": "your_service_key"
})
dust_data = json.loads(dust_response.text)

# Extract relevant weather information
weather_description = weather_data['response']['body']['items']['item'][0]['fcstValue']
current_temp = float(weather_description)
current_humidity = weather_data['response']['body']['items']['item'][1]['fcstValue']
wind_speed = weather_data['response']['body']['items']['item'][3]['fcstValue']
forecast = weather_data['response']['body']['items']['item'][4]['fcstValue']

# Use ChatGPT to generate weather forecast from a 10-year weathercaster's perspective
prompt = f"As a 10-year weathercaster, I predict that today's weather will be {forecast}."
response = openai.Completion.create(
    engine="davinci",
    prompt=prompt,
    max_tokens=100,
    n=1,
    stop=None,
    temperature=0.7,
)
forecast_10_year = response.choices[0].text.strip()

# Determine what clothes to wear based on current temperature
if current_temp < 5:
    clothing_recommendation = "It's very cold, wear a heavy coat, scarf, gloves, and boots."
elif current_temp < 10:
    clothing_recommendation = "It's cold, wear a warm coat, scarf, and boots."
elif current_temp < 15:
    clothing_recommendation = "It's cool, wear a light jacket or sweater."
elif current_temp < 20:
    clothing_recommendation = "It's mild, wear a light jacket or sweater."
elif current_temp < 25:
    clothing_recommendation = "It's warm, wear a t-shirt or blouse."
else:
    clothing_recommendation = "It's hot, wear light clothing."

# Determine the fine dust level
dust_level = int(dust_data['response']['body']['items'][0]['pm10Value'])

if dust_level <= 30:
    dust_recommendation = "The fine dust level is good."
elif dust_level <= 80:
    dust_recommendation = "The fine dust level is moderate. It is recommended to reduce outdoor activities and wear a mask."
elif dust_level <= 150:
    dust_recommendation = "The fine dust level is bad. It is recommended to avoid outdoor activities and wear a mask."
else:
    dust_recommendation = "The fine dust level is very bad. It is recommended to stay indoors and wear a mask."

# Construct the message to be sent by the chatbot
message = f"Good morning! As a 10-year weathercaster, I predict that today's weather will be {forecast_10_year}. The current temperature is {current_temp}°C with a humidity of {current_humidity}% and wind speed of {wind_speed}m/s. {clothing_recommendation} {dust_recommendation}"

# Send the message via KakaoTalk API
headers = {'Authorization': f'Bearer {access_token}'}
data = {'template_object': json.dumps({'text': message})}
response = requests.post(url, headers=headers, data=data)

# Check if the message was sent successfully
if response.status_code == 200:
    print("Message sent successfully!")
else:
    print(f"Error {response.status_code}: {response.text}")
