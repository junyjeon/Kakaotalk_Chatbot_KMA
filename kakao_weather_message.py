import requests
from bs4 import BeautifulSoup

API_KEY = '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'
LOCATION = 'your_location_code'
API_URL = f'http://apis.data.go.kr/1360000/VilageFcstInfoService/getVilageFcst?serviceKey={API_KEY}&numOfRows=10&pageNo=1&base_date=20230423&base_time=0200&nx={LOCATION}&ny={LOCATION}'

def get_weather_data(api_url):
    response = requests.get(api_url)
    soup = BeautifulSoup(response.content, 'xml')
    items = soup.find_all('item')

    weather_data = {}
    for item in items:
        category = item.find('category').text
        value = item.find('fcstValue').text
        if category in ['T1H', 'REH', 'SKY']:
            weather_data[category] = float(value)

    return weather_data

def clothing_recommendation(weather_data):
    temperature = weather_data['T1H']
    humidity = weather_data['REH']
    sky = weather_data['SKY']

    if temperature < 5:
        recommendation = 'Wear a heavy coat, gloves, and a scarf.'
    elif temperature < 12:
        recommendation = 'Wear a jacket and a long-sleeved shirt.'
    elif temperature < 20:
        recommendation = 'Wear a light jacket or a sweater.'
    elif temperature < 30:
        recommendation = 'Wear a short-sleeved shirt and shorts or a skirt.'
    else:
        recommendation = 'Wear lightweight, breathable clothing.'

    if humidity > 80:
        recommendation += ' It is humid, so choose moisture-wicking fabrics.'

    if sky < 4:
        recommendation += ' The sky is clear, don\'t forget sunglasses and sunscreen.'
    elif sky < 7:
        recommendation += ' There might be some clouds, consider taking an umbrella.'
    else:
        recommendation += ' It may rain, bring an umbrella and wear waterproof shoes.'

    return recommendation

if __name__ == '__main__':
    weather_data = get_weather_data(API_URL)
    recommendation = clothing_recommendation(weather_data)
    print(recommendation)
