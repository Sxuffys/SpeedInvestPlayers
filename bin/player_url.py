# Imports
import cloudscraper
from bs4 import BeautifulSoup
import requests, re, random, os, time
import asyncio
from concurrent.futures import ThreadPoolExecutor
import json
import logging
from requests_ip_rotator import ApiGateway


scraper = cloudscraper.CloudScraper()
scraper.trust_env = False


class Proxies:
    def __init__(self, header_file='C:\\Users\\Timo\\PycharmProjects\\SpeedInvestPlayers\\json_data\\data_header_details.json',
                 player_file='C:\\Users\\Timo\\PycharmProjects\\SpeedInvestPlayers\\json_data\\player_urls.json'):

        self.header_file = header_file  # To save Location of where you have saved Json File
        self.player_file = player_file
        self.header_data = json.load(open('C:\\Users\\Timo\\PycharmProjects\\SpeedInvestPlayers\\json_data\\data_header_details.json', 'r'))
        self.player_data = json.load(open('C:\\Users\\Timo\\PycharmProjects\\SpeedInvestPlayers\\json_data\\player_urls.json', 'r'))
        self.def_logger()

    # Definign Logger for this class
    def def_logger(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter('%(asctime)s : %(filename)s : %(funcName)s : %(levelname)s : %(message)s')
        self.file_handler = logging.FileHandler(os.path.abspath('C:\\Users\\Timo\\PycharmProjects\\SpeedInvestPlayers\\log_data\\proxies.log'))
        self.file_handler.setLevel(logging.DEBUG)
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)

    # Function to return Header when called
    def return_header(self):
        header = {
            'user-agent': self.header_data['user_agents_scrap'][random.randint(0, len(self.header_data['user_agents_scrap']) - 1)],
            'referer': self.header_data['referrer'][random.randint(0, len(self.header_data['referrer']) - 1)],
            'Upgrade-Insecure-Requests': '0',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-US,en;q=0.5'
        }

        return header

    # To save json data in disk
    def save_data(self):
        with open(self.player_file, 'w') as outfile:
            json.dump(self.player_data, outfile, indent=4)


class proxy_checker(Proxies):
    def __init__(self):
        Proxies.__init__(self)
        self.check_url = 'https://www.futbin.com/22/playerGraph?type=yesterday&year=22&player=158023&set_id='

    def fetch(self):
        try:
            gateway = ApiGateway(self.check_url)
            gateway.start()
            scraper.mount(self.check_url, gateway)
            with scraper.get(self.check_url, timeout=10, headers=self.return_header()) as response:
                if response.status_code == 200:
                    self.logger.info('SuccessFul Proxy-> {}'.format(response.status_code))
                    return response
                else:
                    self.logger.warning('Status Code {} Captcha Triggered'.format(response.status_code))
                    return '0'
        except Exception as E:
            print(E)
            self.logger.warning('Timeout Proxy-> {}'.format(E))
            return '0'

    async def fetch_urls(self):
        with ThreadPoolExecutor(max_workers=50) as executor:
            loop = asyncio.get_event_loop()
            tasks = [
                loop.run_in_executor(executor, self.fetch)
                for i in range(50)
            ]
            for response in await asyncio.gather(*tasks):
                if response != '0':
                    self.header_data['working_proxies'].append(response.json())

    def async_get_proxies(self):
        try:
            self.loop = asyncio.get_event_loop()
            self.loop.set_debug(1)
            future = asyncio.ensure_future(self.fetch_urls())
            self.loop.run_until_complete(future)
        except Exception as E:
            self.logger.warning(E)
        finally:
            self.loop.close()


if __name__ == "__main__":
    pro = proxy_checker()
    pro.async_get_proxies()
    pro.save_data()
