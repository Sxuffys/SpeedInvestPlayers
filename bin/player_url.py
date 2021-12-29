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
from datetime import date, timedelta


class Price:
    def __init__(self,
                 header_file='C:\\Users\\Timo\\PycharmProjects\\SpeedInvestPlayers\\json_data\\data_header_details.json',
                 player_file='C:\\Users\\Timo\\PycharmProjects\\SpeedInvestPlayers\\json_data\\player_urls.json',
                 hourly_file='C:\\Users\\Timo\\PycharmProjects\\SpeedInvestPlayers\\json_data\\hourly_prices.json',
                 id_file='C:\\Users\\Timo\\PycharmProjects\\SpeedInvestPlayers\\json_data\\player_ids.json'):

        self.hourly_file = hourly_file
        self.header_file = header_file  # To save Location of where you have saved Json File
        self.player_file = player_file
        self.id_file = id_file
        self.header_data = json.load(open('C:\\Users\\Timo\\PycharmProjects\\SpeedInvestPlayers\\json_data\\data_header_details.json', 'r'))
        self.player_data = json.load(open('C:\\Users\\Timo\\PycharmProjects\\SpeedInvestPlayers\\json_data\\player_urls.json', 'r'))
        self.id_data = json.load(open('C:\\Users\\Timo\\PycharmProjects\\SpeedInvestPlayers\\json_data\\player_ids.json', 'r'))
        self.hourly_data = json.load(open('C:\\Users\\Timo\\PycharmProjects\\SpeedInvestPlayers\\json_data\\hourly_prices.json', 'r'))
        self.def_logger()
        self.gateways = 0
        self.total_requests = 0

    # Defining Logger for this class
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
    def save_url_data(self):
        with open(self.player_file, 'w') as outfile:
            json.dump(self.player_data, outfile, indent=4)

    def save_id_data(self):
        with open(self.id_file, 'w') as outfile:
            json.dump(self.id_data, outfile, indent=4)

    def save_price_data(self):
        with open(self.hourly_file, 'w') as outfile:
            json.dump(self.hourly_data, outfile, indent=4)


class PriceScraper(Price):
    def __init__(self):
        Price.__init__(self)
        self.check_url = 'https://www.futbin.com/22/playerGraph?type=yesterday&year=22&player=158023&set_id='
        self.zero_to_fiveK = 'https://www.futbin.com/players?page=1&ps_price=0-5000&version=gold'
        self.url = 'https://www.futbin.com/'
        self.rejects = 0
        self.working_header = {'authority': 'www.futbin.com', 'method': 'GET', 'scheme': 'https', 'accept': 'application/json, text/javascript, */*; q=0.01', 'accept-encoding': 'gzip, deflate, br', 'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7', 'referer': 'https://www.futbin.com/', 'sec-ch-ua': '"Not A;Brand";v="99", "Chromium";v="34", "Google Chrome";v="34"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-origin', 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F', 'x-requested-with': 'XMLHttpRequest'}
        self.working_cookie = {'PHPSESSID': 'cfb7149380441468e88b73eb903febff', 'comments': 'true', 'platform': 'ps4', 'theme_player': 'true'}

    async def create_cookie_token(self, gate):
        try:
            scraper = cloudscraper.create_scraper(interpreter='nodejs')
            scraper.trust_env = False
            scraper.mount(self.url, gate)
            header = self.return_header()
            with scraper.get(self.url, timeout=10, headers=header) as response:
                time.sleep(random.randint(0, 1))
                if response.status_code == 200:
                    self.working_cookie = response.cookies.get_dict()
                    self.working_header = header
                    self.logger.info(f'Got working cookie-> {self.working_cookie}: with header -> {self.working_header}')
                    return True
                else:
                    self.logger.warning(f'Could not create Cookie Error -> {response.status_code}')
                    return False
        except Exception as E:
            self.logger.warning(E)

    async def create_gateway(self):
        try:
            gateway = ApiGateway(self.url)
            gateway.start()
            self.gateways += 1
            return gateway
        except Exception as E:
            self.logger.warning(E)

    def fetch(self, url, gate):
        try:
            time.sleep(random.randint(0, 5))
            scraper = cloudscraper.create_scraper(interpreter='nodejs')
            scraper.trust_env = False
            scraper.mount(self.url, gate)
            with scraper.get(url, timeout=10, headers=self.working_header, cookies=self.working_cookie) as response:
                if response.status_code == 200:
                    self.total_requests += 1
                    self.logger.info(f'Successfully fetched -> {response.status_code}')
                    self.player_data['fetched_page_urls'].append(url)
                    #self.player_data['not_fetched_page_urls'].remove(url)
                    return response
                else:
                    self.logger.warning(f'Status Code {response.status_code} Captcha Triggered')
                    return '0'
        except Exception as E:
            self.logger.warning(f'Error: {E}')
            return '0'

    async def fetch_urls(self):
        try:
            gate = await self.create_gateway()
            ret = await self.create_cookie_token(gate)
            while not ret:
                ret = await self.create_cookie_token(gate)
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
            print('done fetching urls')
            self.save_url_data()
        except Exception as E:
            self.logger.warning(E)

    def fetch_id(self, names_and_ids, gate, i):
        try:
            url = f'https://www.futbin.com/22/getTp?pid={names_and_ids[i][0]}&type=player'
            time.sleep(random.randint(0, 5))
            scraper = cloudscraper.create_scraper(interpreter='nodejs')
            scraper.trust_env = False
            scraper.mount(self.url, gate)
            with scraper.get(url, timeout=10, headers=self.working_header, cookies=self.working_cookie) as response:
                if response.status_code == 200:
                    self.total_requests += 1
                    name = names_and_ids[i][1]
                    ea_id = names_and_ids[i][0]
                    futbin_id = response.json()['data']['g'][1]
                    self.logger.info(f'Successfully fetched -> {response.status_code}')
                    self.player_data['player_urls'].remove(names_and_ids[i][2])
                    #{ea_id: {str(date.today()): ps}}
                    return {"Name": name, "ea_id": ea_id, "futbin_id": futbin_id}
                else:
                    self.logger.warning(f'Status Code {response.status_code}: Captcha Triggered')
                    return '0'
        except Exception as E:
            self.logger.warning(f'Error: {E}')
            return '0'

    async def fetch_ids(self):
        names_ids = []
        for url in self.player_data['player_urls']:
            s = url.split('/')
            id = s[3]
            name = s[4]
            names_ids.append((id, name, url))
        while self.player_data['player_urls']:
            gate = await self.create_gateway()
            ret = await self.create_cookie_token(gate)
            while not ret:
                ret = await self.create_cookie_token(gate)
            with ThreadPoolExecutor(max_workers=100) as executor:
                loop = asyncio.get_event_loop()
                tasks = [
                    loop.run_in_executor(executor, self.fetch_id, names_ids, gate, i)
                    for i in range(0, len(names_ids))
                ]
            gate.shutdown()
            for response in await asyncio.gather(*tasks):
                if response != 0:
                    self.id_data['ids'].append(response)
        print('Done fetching ids')
        self.save_id_data()

    def return_hourly_link(self, num, futbin_id):
        if num == 0:
            return f'https://www.futbin.com/22/playerGraph?type=today&year=22&player={futbin_id}&set_id='
        elif num == 1:
            return f'https://www.futbin.com/22/playerGraph?type=yesterday&year=22&player={futbin_id}&set_id='
        else:
            return f'https://www.futbin.com/22/playerGraph?type=da_yesterday&year=22&player={futbin_id}&set_id='

    def fetch_price(self, data, gate):
        try:
            url = data[0]
            ea_id = data[1]
            time.sleep(random.randint(0, 7))
            scraper = cloudscraper.create_scraper(interpreter='nodejs')
            scraper.trust_env = False
            scraper.mount(self.url, gate)
            with scraper.get(url, timeout=10, headers=self.working_header, cookies=self.working_cookie) as response:
                if response.status_code == 200:
                    self.total_requests += 1
                    self.logger.info(f'Successfully fetched -> {response.status_code}')
                    datas = (response.json(), ea_id)
                    return datas
                else:
                    self.logger.warning(f'Status Code {response.status_code} Captcha Triggered')
                    return '0'
        except Exception as E:
            self.logger.warning(f'Error: {E}')
            return '0'

    async def fetch_prices(self):
        try:
            for i in range(0, 3):
                hourly_urls = []
                for p_data in self.id_data['ids']:
                    hourly_urls.append((self.return_hourly_link(i, p_data["futbin_id"]), p_data["ea_id"]))
                gate = await self.create_gateway()
                ret = await self.create_cookie_token(gate)
                while not ret:
                    ret = await self.create_cookie_token(gate)
                with ThreadPoolExecutor(max_workers=300) as executor:
                    loop = asyncio.get_event_loop()
                    tasks = [
                        loop.run_in_executor(executor, self.fetch_price, data_set, gate)
                        for data_set in hourly_urls
                    ]
                gate.shutdown()
                for data in await asyncio.gather(*tasks):
                    if data != '0':
                        price = data[0]
                        ea_id = data[1]
                        if price.get('ps') is not None:
                            ps = price['ps']
                            if self.hourly_data['prices'].get(ea_id) is None:
                                key_value = {ea_id: {str(date.today() - timedelta(days=i)): ps}}
                                self.hourly_data['prices'].update(key_value)
                            else:
                                key_value = {str(date.today() - timedelta(days=i)): ps}
                                self.hourly_data['prices'][ea_id].update(key_value)
                        else:
                            pass
            print('done fetching prices')
            self.save_price_data()
        except Exception as E:
            self.logger.warning(E)

    async def run(self):
        try:
            await self.fetch_urls()
            await self.fetch_ids()
            await self.fetch_prices()
        except Exception as E:
            self.logger.warning(E)

    def async_run(self):
        try:
            self.loop = asyncio.get_event_loop()
            self.loop.set_debug(True)
            future = asyncio.ensure_future(self.run())
            self.loop.run_until_complete(future)
        except Exception as E:
            self.logger.warning(E)
        finally:
            self.loop.close()


if __name__ == "__main__":
    pro = PriceScraper()
    pro.async_run()
    print(pro.total_requests)
    print(pro.gateways)
