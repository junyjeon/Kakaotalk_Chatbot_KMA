import requests

CLIENT_ID = "a9cfd4733d9e91bf1becfe22f8c65fa7"
CLIENT_SECRET = "a9cfd4733d9e91bf1becfe22f8c65fa7"
REDIRECT_URI = "https://localhost:3000"

AUTH_URL = f"https://kauth.kakao.com/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=talk_message"

response = requests.get(AUTH_URL)
# print('response: ', response)
# print('response.headers: ', response.headers)
# print('response.data: ', response.content)

authorization_code = input(f"Please visit the following URL to authorize your application:\n{AUTH_URL}\nEnter the authorization code: ")

TOKEN_URL = "https://kauth.kakao.com/oauth/token"
data = {
    "grant_type": "authorization_code",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "redirect_uri": REDIRECT_URI,
    "code": authorization_code
}

response = requests.post(TOKEN_URL, data=data)
access_token = response.json()["access_token"]
print(f"Access token: {access_token}")