import requests
from time import sleep
import time
import datetime

#import I2C_LCD_Driver
#mylcd = I2C_LCD_Driver.lcd()

# Fuel Rat api Rescue URL
rescue_url = "https://api.fuelrats.com/rescues"
headers = {"Authorization": "Bearer Key"}


def get_data(url):
    try:
        data = requests.get(url, headers=headers).json()
        data = data['data']
        return [dta['attributes'] for dta in data if dta['attributes']['status'] == 'open']
    except requests.exceptions.RequestException:
        sleep(5)
        data = requests.get(url, headers=headers).json()
        data = data['data']
        return [dta['attributes'] for dta in data if dta['attributes']['status'] == 'open']


# function to convert string datetime value when rescue commenced (usually entered by Mecha)
def dte_convert(dte):
    d1 = datetime.datetime.strptime(dte, "%Y-%m-%dT%H:%M:%S.%fZ") + datetime.timedelta(hours=10)
    d2 = datetime.datetime.now()  # set variable to current dateTime
    dur_s = (d2 - d1).total_seconds()  # similar to datediff and calculates to seconds
    dy = divmod(dur_s, 86400)
    hrs = divmod(dy[1], 3600)
    mins = divmod(hrs[1], 60)
    ret = '%d d %d h %d m' % (dy[0], hrs[0], mins[0])
    return ret


while True:
    json_data = get_data(rescue_url)

    if json_data:
        for each in json_data:

            client = each['client']
            platform = each['platform']
            code_red = each['codeRed']
            system = each['system']
            active = dte_convert(each['createdAt'])

            print("C: %s" % client)
            print("P: %s" % platform + " CR: %s" % code_red)
            print("S: %s" % system)
            print("A: %s" % str(active))

#            mylcd.lcd_display_string("C: %s" %client ,1)
#            mylcd.lcd_display_string("P: %s" %platform + "CR: %s" %str(cde_red), 2)
#            mylcd.lcd_display_string("S: %s" %system, 1)
#            mylcd.lcd_display_string("A: %s" %str(res_datetime), 2)

    else:
            print("Date: %s" % time.strftime("%d/%m/%Y"))
            print("Time: %s" % time.strftime("%H:%M"))
            print('No Active Rescues')

    sleep(5)

#         #   mylcd.lcd_display_string("Date: %s" %time.strftime("%d/%m/%Y"), 1)
#         #   mylcd.lcd_display_string("Time: %s" %time.strftime("%H:%M:%S"), 2)
#           # mylcd.lcd_display_string('No Active Rescues', 3)





