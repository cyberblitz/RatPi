import requests
import pickle


def create_cookie():

    s = requests.Session()

    url = "https://api.fuelrats.com/login"
    param = {"email": "username", "password": "password"}

    response = s.post(url, json=param)

    with open('ratCookie', 'wb') as f:
        pickle.dump(response.cookies, f)
    import ratRescues


 # create_cookie()

