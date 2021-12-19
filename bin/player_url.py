# Imports
import cloudscraper
from bs4 import BeautifulSoup
import requests, re, random, os, time
import asyncio
from concurrent.futures import ThreadPoolExecutor
import json
import logging
from requests_ip_rotator import ApiGateway
from fake_useragent import UserAgent


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
        self.gateways = 0

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
        ua = UserAgent()
        header = {
            'user-agent': str(ua.random),
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
        self.zero_to_fiveK = 'https://www.futbin.com/players?page=1&ps_price=0-5000&version=gold'

    def fetch(self, url):
        try:
            gateway = ApiGateway(url)
            gateway.start()
            self.gateway = gateway
            scraper.mount(url, gateway)
            self.gateways += 1
            with scraper.get(url, timeout=10, headers=self.return_header()) as response:
                if response.status_code == 200:
                    self.logger.info('SuccessFul Proxy-> {}'.format(response.status_code))
                    self.gateway.close()
                    return response
                else:
                    self.gateway.close()
                    self.logger.warning('Status Code {} Captcha Triggered'.format(response.status_code))
                    return '0'
        except Exception as E:
            print(E)
            self.gateway.close()
            self.logger.warning('Timeout Proxy-> {}'.format(E))
            return '0'

    async def fetch_urls(self):
        urls = self.player_data['page_urls']
        with ThreadPoolExecutor(max_workers=50) as executor:
            loop = asyncio.get_event_loop()
            #for page in range(1, 58):
            #    expls_url = f'https://www.futbin.com/players?page={page}&ps_price=0-5000&version=gold'
            tasks = [
                loop.run_in_executor(executor, self.fetch, url)
                for url in urls
            ]
            for response in await asyncio.gather(*tasks):
                if response != '0':
                    soup = BeautifulSoup(response.text, features="lxml")
                    numbers = [1, 2]
                    players = soup.findAll('tr')
                    for link in players:
                        p = link.get('data-url')
                        self.player_data['player_urls'].append(p)

    def async_get_proxies(self):
        try:
            self.loop = asyncio.get_event_loop()
            self.loop.set_debug(True)
            future = asyncio.ensure_future(self.fetch_urls())
            self.loop.run_until_complete(future)
        except Exception as E:
            self.logger.warning(E)
        finally:
            self.loop.close()

    def help(self):
        res = scraper.get(self.zero_to_fiveK, timeout=10, headers=self.return_header())
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, features='lxml')
            pages = soup.findAll('.page-link')
            sistaSidan = (len(pages))
            return sistaSidan
        else:
            print(res.text)
            return "0"


if __name__ == "__main__":
    pro = proxy_checker()
    pro.async_get_proxies()
    print(pro.gateways)
    pro.save_data()
    #req = pro.help()
    #if req == '0':
    #    print('cap')
    #else:
    #    print(req)
