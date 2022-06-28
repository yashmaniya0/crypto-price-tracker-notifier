from win10toast import ToastNotifier
import requests
import time
import logging
import webbrowser
import json
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')  # we can send 10,000 requests per day
                                # uses Live Coin Watch API

toaster = ToastNotifier()
print('Toaster is on!')

def stalk(coin = 'BTC', target = 5000000, sleep_time = 60):

    def make_logger(logger_name, log_file, level=logging.INFO):
        l = logging.getLogger(logger_name)
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        fileHandler = logging.FileHandler(log_file, mode='w')
        fileHandler.setFormatter(formatter)
        # streamHandler = logging.StreamHandler()
        # streamHandler.setFormatter(formatter)
        l.setLevel(level)
        l.addHandler(fileHandler)
        # l.addHandler(streamHandler)    

        logger = logging.getLogger(logger_name)
        logger.propagate = False

        return logger

    def extract_price(coin:str):
                                                            
        url = "https://api.livecoinwatch.com/coins/single"
        payload = json.dumps({
        "currency": "INR",
        "code": coin,
        "meta": False
        })
        headers = {
        'content-type': 'application/json',
        'x-api-key': API_KEY
        }

        response = requests.request("POST", url, headers=headers, data=payload).text
        data = json.loads(response)
        curr_price = data['rate']

        return curr_price

    def send_notif(curr_price):
        target_link = 'https://wazirx.com/exchange/' + coin + '-INR'

        toaster.show_toast(title = f"Alert!!! Target for {coin} reached.\nCurrent Price is {curr_price} INR", msg = target_link ,
	                   duration=10 , callback_on_click = lambda : webbrowser.open_new(target_link))

    coin = coin.upper()

    logger_0 = make_logger('log0', f'./{coin}1min.log')
    logger_1 = make_logger('log1', f'./{coin}10mins.log')
    logger_2 = make_logger('log2', f'./{coin}1hr.log')
    secs = 0

    check_up = False
    initial_price = extract_price(coin)
    if initial_price < target:
        check_up = True

    logger_0.info(f'Initial Price : {initial_price}')
    logger_1.info(f'Initial Price : {initial_price}')
    logger_2.info(f'Initial Price : {initial_price}')

    while 1:
        time.sleep(sleep_time)
        secs += sleep_time

        curr_price = extract_price(coin)

        if check_up:
            if curr_price>=target:
                send_notif(curr_price)
        else:
            if curr_price<=target:
                send_notif(curr_price)

        if secs%60==0:
            logger_0.info(curr_price)
        if secs%(10*60)==0:
            logger_1.info(curr_price)
        if secs%(60*60)==0:
            logger_2.info(curr_price)


# here goes the command
stalk(coin = 'rune', target = 170, sleep_time = 60)