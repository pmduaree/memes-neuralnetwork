import requests.auth

app_id = '8wkuvZHt1Fhd4w'
app_secret = '2wR5SbBDC_4p8IjJBhEWHaP3H_0'
username = "username_random_1"
password = "random123"


def log_in_and_get_headers():
    client_auth = requests.auth.HTTPBasicAuth(app_id, app_secret)
    post_data = {"grant_type": "password", "username": username, "password": password}
    headers = {"User-Agent": "localhost/0.1 by " + username}
    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data,
                             headers=headers)
    access_token = response.json()['access_token']
    bearer = "bearer " + access_token

    headers = {"Authorization": bearer, "User-Agent": "localhost/0.1 by " + username}
    return headers
