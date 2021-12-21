# Imports
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
from yggtorrentscraper import YggTorrentScraperSelenium
from selenium import webdriver



h = {'Date': 'Tue, 21 Dec 2021 14:51:23 GMT',
     'Content-Type': 'text/html; charset=UTF-8',
     'Content-Length': '24959',
     'Connection': 'keep-alive',
     'x-amzn-RequestId': 'e6d25464-6db4-4933-9c9f-a8103b3881ab',
     'CF-RAY': '6c11eda0ebcedfe7-FRA',
     'access-control-allow-origin': '*',
     'Expect-CT': 'max-age=604800,'' report-uri="https://report-uri.cloudflare.com/cdn-cgi/beacon/expect-ct"',
    'Content-Encoding': 'gzip',
     'CF-Cache-Status': 'DYNAMIC',
     'x-amzn-Remapped-Connection': 'keep-alive',
     'x-amz-apigw-id': 'KtF82HGdliAFjxw=',
     'vary': 'Accept-Encoding',
     'x-amzn-Remapped-Server': 'cloudflare',
     'x-powered-by': 'PHP/7.2.22',
     'x-amzn-Remapped-Date': 'Tue, 21 Dec 2021 14:51:23 GMT'}

class Proxies:
    def __init__(self, header_file='C:\\Users\\Timo\\PycharmProjects\\SpeedInvestPlayers\\json_data\\data_header_details.json',
                 player_file='C:\\Users\\Timo\\PycharmProjects\\SpeedInvestPlayers\\json_data\\player_urls.json'):

        self.header_file = header_file  # To save Location of where you have saved Json File
        self.player_file = player_file
        self.header_data = json.load(open('C:\\Users\\Timo\\PycharmProjects\\SpeedInvestPlayers\\json_data\\data_header_details.json', 'r'))
        self.player_data = json.load(open('C:\\Users\\Timo\\PycharmProjects\\SpeedInvestPlayers\\json_data\\player_urls.json', 'r'))
        self.def_logger()
        self.gateways = 0
        self.count_gate = 0

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
        chrome = ua.chrome
        splitted = chrome.split('/')
        version = splitted[3][:2]
        header = {
            'authority': 'www.futbin.com',
            'method': 'GET',
            'scheme': 'https',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
            #'Cookie': 'pc=true; ps=true; xbox=true; cookieconsent_status=dismiss; PHPSESSID=4ijtnhr6vacmjp1ppg9e57q280; theme_player=true; comments=true; platform=ps4',
            'referer': 'https://www.futbin.com/',
            'sec-ch-ua': f'"Not A;Brand";v="99", "Chromium";v="{version}", "Google Chrome";v="{version}"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': str(chrome),
            'x-requested-with': 'XMLHttpRequest'
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
        self.url = 'https://www.futbin.com/'
        self.rejects = 0
        self.h = {'authority': 'www.futbin.com', 'method': 'GET', 'scheme': 'https', 'accept': 'application/json, text/javascript, */*; q=0.01', 'accept-encoding': 'gzip, deflate, br', 'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7', 'referer': 'https://www.futbin.com/', 'sec-ch-ua': '"Not A;Brand";v="99", "Chromium";v="34", "Google Chrome";v="34"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-origin', 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F', 'x-requested-with': 'XMLHttpRequest'}
        self.cookie = {'PHPSESSID': 'cfb7149380441468e88b73eb903febff', 'comments': 'true', 'platform': 'ps4', 'theme_player': 'true'}

    def fetch(self, url, gate):
        try:
            time.sleep(random.randint(0, 5))
            header = self.return_header()
            ua = header['user-agent']
            scraper = cloudscraper.create_scraper(interpreter='nodejs')
            scraper.trust_env = False
            scraper.mount(self.url, gate)
            with scraper.get(url, timeout=10, headers=self.h, cookies=self.cookie) as response:
                if response.status_code == 200:
                    print(response.cookies.get_dict())
                    print(header)
                    self.logger.info('SuccessFul Proxy-> {}'.format(response.status_code))
                    self.player_data['fetched_page_urls'].append(url)
                    self.player_data['not_fetched_page_urls'].remove(url)
                    return response
                else:
                    #if retries > 0:
                    #    self.fetch(url, gate, retries - 1)
                    self.logger.warning('Status Code {} Captcha Triggered'.format(response.status_code))
                    return '0'
        except Exception as E:
            print(E)
            self.logger.warning('Timeout Proxy-> {}'.format(E))
            return '0'

    async def fetch_urls(self):
        urls = []
        for url in self.player_data['not_fetched_page_urls']:
            urls.append(url)
        while self.player_data['not_fetched_page_urls']:
            time.sleep(1)
            #five_urls = urls[:5]
            #for i in range(0, 4):
            #    urls.pop(i)
            length = len(self.player_data['not_fetched_page_urls'])
            print(length)
            gate = await self.create_gateway()
            with ThreadPoolExecutor(max_workers=57) as executor:
                loop = asyncio.get_event_loop()
                tasks = [
                    loop.run_in_executor(executor, self.fetch, url, gate)
                    for url in self.player_data['not_fetched_page_urls']
                ]
            gate.shutdown()
            for response in await asyncio.gather(*tasks):
                if response != '0':
                    soup = BeautifulSoup(response.text, features="lxml")
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

    async def create_gate_list(self, length):
        gates = []
        for i in range(length//5 + 1):
            gates.append(await self.create_gateway())
            time.sleep(2)
        return gates

    # TODO: SEE THIS ____________________________________________________________________
    async def create_gateway(self):
        try:
            gateway = ApiGateway(self.url)
            gateway.start()
            self.gateways += 1
            return gateway
        except Exception as E:
            self.logger.warning(E)

    def get_ids(self):
        for url in self.player_data['player_urls']:
            s = url.split("/")
            pid = s[3]
            self.player_data['player_ids'].append(pid)

    def get_graph_url(self):
        for player_id in self.player_data['player_ids']:
            today_hourly_url = f'https://www.futbin.com/22/playerGraph?type=today&year=22&player={player_id}&set_id='
            yesterday_hourly_url = f'https://www.futbin.com/22/playerGraph?type=yesterday&year=22&player={player_id}&set_id='
            da_yesterday_hourly_url = f'https://www.futbin.com/22/playerGraph?type=da_yesterday&year=22&player={player_id}&set_id='
            urls = [today_hourly_url, yesterday_hourly_url, da_yesterday_hourly_url]
            self.player_data['not_fetched_graph_urls'].append(urls)

    def fetch_g(self, url, i):
        try:
            scraper = cloudscraper.CloudScraper()
            scraper.trust_env = False
            scraper.mount(self.url, self.gateway)
            with scraper.get(url, timeout=10, headers=self.return_header()) as response:
                if response.status_code == 200:
                    self.logger.info('SuccessFul Proxy-> {}'.format(response.status_code))
                    self.player_data['not_fetched_graph_urls'][i].remove(url)
                    if len(self.player_data['not_fetched_graph_urls'][i]) == 0:
                        self.player_data['not_fetched_graph_urls'].pop(i)
                    self.gateway.shutdown()
                    return response
                else:
                    self.gateway.shutdown()
                    self.logger.warning('Status Code {} Captcha Triggered'.format(response.status_code))
                    return '0'
        except Exception as E:
            print(E)
            self.gateway.close()
            self.logger.warning('Timeout Proxy-> {}'.format(E))
            return '0'

    async def fetch_graph(self):
        while self.player_data['not_fetched_graph_urls']:
            self.create_gateway()
            for i in range(len(self.player_data['not_fetched_graph_urls'])):
                with ThreadPoolExecutor(max_workers=50) as executor:
                    loop = asyncio.get_event_loop()
                    tasks = [
                        loop.run_in_executor(executor, self.fetch_g, url, i)
                        for url in self.player_data['not_fetched_graph_urls'][i]
                    ]
                    for response in await asyncio.gather(*tasks):
                        if response != '0':
                            self.player_data['player_prices'].append(response.json())

    def async_get_prices(self):
        try:
            self.loop = asyncio.get_event_loop()
            self.loop.set_debug(True)
            future = asyncio.ensure_future(self.fetch_graph())
            self.loop.run_until_complete(future)
        except Exception as E:
            self.logger.warning(E)
        finally:
            self.loop.close()





if __name__ == "__main__":
    pro = proxy_checker()
    pro.async_get_proxies()
    #pro.get_ids()
    #pro.get_graph_url()
    #pro.async_get_prices()
    print(pro.gateways)
    pro.save_data()
