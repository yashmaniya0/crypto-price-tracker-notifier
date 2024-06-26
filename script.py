from win10toast import ToastNotifier
import requests
import time
import logging
import webbrowser
import json
import os

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
                                                            
        url = "https://api.wazirx.com/sapi/v1/ticker/24hr?symbol=" + coin.lower() + "inr"

        response = requests.get(url).text
        data = json.loads(response)
        curr_price = data['lastPrice']

        return float(curr_price)

    def send_notif(curr_price):
        target_link = 'https://wazirx.com/exchange/' + coin.lower() + '-INR'

        toaster.show_toast(title = f"Alert!!! Target for {coin.upper()} reached.\nCurrent Price is {curr_price} INR", msg = target_link ,
	                   duration=10 , callback_on_click = lambda : webbrowser.open_new(target_link))


    logger_0 = make_logger('log0', f'./{coin.upper()}_1min.log')
    logger_1 = make_logger('log1', f'./{coin.upper()}_10mins.log')
    logger_2 = make_logger('log2', f'./{coin.upper()}_1hr.log')
    secs = 0

    check_up = False
    initial_price = extract_price(coin)
    if initial_price < target:
        check_up = True

    logger_0.info(f'{coin.upper()} -> INR\n')
    logger_1.info(f'{coin.upper()} -> INR\n')
    logger_2.info(f'{coin.upper()} -> INR\n')

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


crypto = input('Crypto Code :\t')
target = float(input('Set Limit :\t'))

# here goes the command
stalk(coin = crypto, target = target, sleep_time = 60)