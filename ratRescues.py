import requests
from time import sleep
import time
import datetime
# import I2C_LCD_Driver

# mylcd = I2C_LCD_Driver.lcd()

# Fuel Rat api Rescue URL
rescue_url = "https://api.fuelrats.com/rescues"
headers = {"Authorization": "Bearer Key"}


# function to extract JSON from Rescue API end point.
def get_data(url):
    data = requests.get(url, headers=headers)  # json()
    if data.status_code == 200:
        data = data.json()
        return data
    else:
        print(data.text)
        print(data.status_code)


# function to convert string datetime value when rescue commenced (usually entered by Mecha)
def dte_convert(dte):
    dte_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    delta_dte = datetime.timedelta(hours=10)
    dur_secs = (datetime.datetime.now() - datetime.datetime.strptime(dte, dte_format) + delta_dte).total_seconds()
    dy = divmod(dur_secs, 86400)
    hrs = divmod(dy[1], 3600)
    mins = divmod(hrs[1], 60)
    ret = '%d d %d h %d m' % (dy[0], hrs[0], mins[0])
    return ret


def stand_by():
    i = 0
    while True:
        i += 1
        print("Date: %s" % time.strftime("%d/%m/%Y"))
        print("Time: %s" % time.strftime("%H:%M:%S"))
        print('No Active Rescues')
        # mylcd.lcd_display_string("Date: %s" % time.strftime("%d/%m/%Y"), 1)
        # mylcd.lcd_display_string("Time: %s" % time.strftime("%H:%M:%S"), 2)
        # mylcd.lcd_display_string('No Active Rescues', 3)
        if i == 5:
            main()


def main():
    while True:
        json_data = get_data(rescue_url)
        for each in json_data['data']:
            stat = each['attributes']['status']
            platform = each['attributes']['platform']

            if stat != 'open':  # and platform == 'ps':

                client = each['attributes']['client']
                cde_red = each['attributes']['codeRed']
                system = each['attributes']['system']
                res_datetime = dte_convert(each['attributes']['createdAt'])

                #  mylcd.lcd_display_string("C: %s" % client, 1)
                #  mylcd.lcd_display_string("P: %s" % platform + "CR: %s" % str(cde_red), 2)
                #  mylcd.lcd_display_string("S: %s" % system, 3)
                #  mylcd.lcd_display_string("A: %s" % str(res_datetime), 4)

                print("C: %s" % client)
                print("P: %s" % platform + "CR: %s" % str(cde_red))
                print("S: %s" % system)
                print("A: %s" % str(res_datetime))
                #sleep(3)


main()
