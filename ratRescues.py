import requests
import datetime
from time import sleep
import time
from threading import Thread
import I2C_LCD_Driver
mylcd = I2C_LCD_Driver.lcd()


json_dataG = []
mylcd.lcd_clear()

def get_data():

    global json_dataG
    while True:
        try:
            fin = []
            rescue_url = "https://api.fuelrats.com/rescues?[status]=open"  # ?$not[status]=closed"
            headers = {"Authorization": "Bearer Key"}
            data = requests.get(rescue_url, headers=headers).json()
            data = data['data']
            json_data = [dta['attributes'] for dta in data]
            if json_data:
                for each in json_data:
                    fin_val = ["C: %s" % each['client'],
                               "P: %s" % each['platform'] + " CR: %s" % each['codeRed'],
                               "S: %s" % each['system'],
                               "A: %s" % dte_convert(each['createdAt'])]
                    fin.append(fin_val)
            else:
                fin = None
            if fin != json_dataG:
                json_dataG = fin
            sleep(5)

        except requests.exceptions.Timeout:
            continue
        except requests.exceptions.ConnectionError:
            continue


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




def clock():
        fin_val = ("Date: %s" % time.strftime("%d/%m/%Y"),
                   "Time: %s" % time.strftime("%H:%M:%S"),
                   'No Active Rescues',
                   '        <^__)~')

        return fin_val

def lcd_scroll(ln3, num_cols):
    sleep(0.5)
    mylcd.lcd_display_string(ln3[:num_cols],3)
    for i in range(len(ln3) - num_cols + 1):
        text_to_print = "S: " + ln3[i:i+num_cols]
        mylcd.lcd_display_string(text_to_print,3)
        #time.sleep(0.2)

def lcd_data(in_data):
    num_cols = 17
    
    ln1, ln2, ln3, ln4 = in_data

       
    mylcd.lcd_display_string(ln1, 1)
    mylcd.lcd_display_string(ln2, 2)
    mylcd.lcd_display_string(ln3[:20], 3)
    mylcd.lcd_display_string(ln4, 4)
    
    if(len(ln3) > num_cols):
        ln3.replace("S: ", "")
        lcd_scroll(ln3, num_cols)

    #print(ln1)
    #print(ln2)
    #print(ln3)
    #print(ln4)


def main():
    i = 0
    varHold = ()
    while True:
        try:
            global json_dataG
            t_clock = clock()
            if json_dataG is not None:
                i = 1
                for data in json_dataG:
                    lcd_data(data)
                    sleep(3)
                    data3 = data[1:3]
                    if data3 != varHold:
                        mylcd.lcd_clear()
                    varHold = data3
            else:
                if i > 0:
                    mylcd.lcd_clear()
                    i = 0
                lcd_data(t_clock)
        except ValueError:
            continue

t1 = Thread(target=get_data)
t2 = Thread(target=main)
t1.start()
t2.start()
