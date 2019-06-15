import requests
import pickle
from time import sleep
import datetime
import ratLoginCookieAuth

# Fuel Rat api Rescue URL
rescue_url = "https://api.fuelrats.com/rescues


# function to extract JSON from Rescue API end point. Here is were the cookie is injected to authenticate
def get_data(url):

    s = requests.Session()
    data = s.get(url, cookies=ratcookie)  # .json()
    if data.status_code == 200:
        data = data.json()
        return data
    elif data.status_code == 400:
        print('creating cookie')
        ratLoginCookieAuth.create_cookie()
    else:
        print(data.text)
        print(data.status_code)


# function to convert string datetime value when rescue commenced (usually entered by Mecha)
def dte_convert(dte):
    rem_t = dte.replace('T', ' ')  # removes 'T' from string with ' '
    rem_z = rem_t.replace('Z', '')  # removes 'Z' from string with '' < important: no space
    con_dte = datetime.datetime.strptime(rem_z, "%Y-%m-%d %H:%M:%S.%f") #
    d1 = con_dte + datetime.timedelta(hours=10)  # similar to a dateadd fx
    d2 = datetime.datetime.now()  # set variable to current dateTime
    dur_s = (d2 - d1).total_seconds()  # similar to datediff and calculates to seconds
    dy = divmod(dur_s, 86400)
    hrs = divmod(dy[1], 3600)
    mins = divmod(hrs[1], 60)
    ret = '%d days %d hours %d mins' % (dy[0], hrs[0], mins[0])
    return ret

# access saved file containing cookie. Cookie Created in ratLoginCookieAuth.py
try:
    with open('ratCookie', 'rb') as f:
        ratcookie = pickle.load(f)

    while True:
        json_data = get_data(rescue_url)

        for each in json_data['data']:
            stat = each['attributes']['status']
            platform = each['attributes']['platform']
            if stat == 'open' and platform == 'ps':
                client = each['attributes']['client']
                cde_red = each['attributes']['codeRed']
                system = each['attributes']['system']
                res_datetime = dte_convert(each['attributes']['createdAt'])
                print(client + ' ' + platform + ' ' + system + ' ' + str(cde_red) + ' ' + stat + ' ' + str(res_datetime))
            else:
                print('No Rescues')
                break
        sleep(5)

except IOError:
    print('creating cookie')
    ratLoginCookieAuth.create_cookie()




