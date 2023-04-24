import requests
import json
import matplotlib.pyplot as plt

url='http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
key='+OkWyS+jCSbH8iy6EgVNtvfDxfKo9ImIII2zL/qdiWXOzs0u5aNFjpZ782duf46IjgD99p9VA5BmiSS8IeosQw=='
para={'serviceKey':key, 'pageNo':'1', 'numOfRows':'1000', 'dataType':'JSON', 'base_date':'20230423', 'base_time':'1400', 'nx':'60', 'ny':'127'}

res = requests.get(url, params=para)
print("1\n")

rew_json = json.loads(res.content);
items = rew_json['response']['body']['items']['item']
print("2\n")
temperture = []
time = []

print("3\n")
for i in items:
	if i['fcstDate'] == '20230423' and i['category'] == 'TMP':
		temperture.append(i['fcstValue'])
		time.append(i['fcstTime'][:2])

print("4\n")
plt.figure(figsize=(12,6))
print("6\n")
plt.rc('font', family='Malgun Gothic')
print("7\n")
plt.title('기상청 날씨 정보', fontsize=20)
print("8\n")
plt.plot(time, temperture)
print("9\n")
plt.xlabel('시간[시]')
print("10\n")
plt.ylabel('기온[℃]')
print("11\n")
plt.show()
print("12\n")
