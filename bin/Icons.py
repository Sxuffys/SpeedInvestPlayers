import cfscrape
import cloudscraper
from bs4 import BeautifulSoup
import requests, re, random, os, time
import asyncio
from concurrent.futures import ThreadPoolExecutor
import json
import logging
from requests_ip_rotator import ApiGateway
from fake_useragent import UserAgent
from datetime import date, timedelta
import heapq
import pandas as pd

class Price:
    def __init__(self,
                 hourly_file='C:\\Users\\Timo\\PycharmProjects\\SpeedInvestPlayers\\json_data\\hourly_prices.json',
                 min_file='C:\\Users\\Timo\\PycharmProjects\\SpeedInvestPlayers\\json_data\\mins_maxs.json'):

        self.hourly_file = hourly_file
        self.min_file = min_file
        self.hourly_data = json.load(open('C:\\Users\\Timo\\PycharmProjects\\SpeedInvestPlayers\\json_data\\hourly_prices.json', 'r'))
        self.min_data = json.load(open('C:\\Users\\Timo\\PycharmProjects\\SpeedInvestPlayers\\json_data\\mins_maxs.json', 'r'))
        self.def_logger()
        self.gateways = 0
        self.counts = []

    def save_min_data(self):
        with open(self.min_file, 'w') as outfile:
            json.dump(self.min_data, outfile, indent=4)

    # Defining Logger for this class
    def def_logger(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter('%(asctime)s : %(filename)s : %(funcName)s : %(levelname)s : %(message)s')
        self.file_handler = logging.FileHandler(os.path.abspath('C:\\Users\\Timo\\PycharmProjects\\SpeedInvestPlayers\\log_data\\main.log'))
        self.file_handler.setLevel(logging.DEBUG)
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)

    def compute_min_max(self):
        for players in self.hourly_data['prices']:
            for day in self.hourly_data['prices'][players]:
                today = self.hourly_data['prices'][players][day]
                smallest = today[0][1]
                greatest = today[0][1]
                for value in today:
                    if value[1] < smallest:
                        smallest = value[1]
                    if value[1] > greatest:
                        greatest = value[1]
                diff = greatest - smallest
                if self.min_data['min_max'].get(players) is None:
                    key_value = {players: {day: [smallest, greatest, diff]}}
                    self.min_data['min_max'].update(key_value)
                else:
                    key_value = {day: [smallest, greatest, diff]}
                    self.min_data['min_max'][players].update(key_value)

    def see(self):
        print(pd.Series(self.hourly_data['prices']["733"]))

df = pd.read_json("C:\\Users\\Timo\\PycharmProjects\\SpeedInvestPlayers\\json_data\\Icon_prices.json")
df.info()
print(pd.DataFrame(df))
#p = Price()
#p.see()
