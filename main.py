from bs4 import BeautifulSoup
import cloudscraper
import cloudscraper
import random
import requests
import time
from bs4 import BeautifulSoup
from requests_ip_rotator import ApiGateway
import random_user_agent
import user_agents
from fake_useragent import UserAgent
import certifi
import urllib3
import undetected_chromedriver.v2 as uc
import requests_html
from urllib3 import Retry
from requests.adapters import HTTPAdapter
from selenium import webdriver
import cfscrape


url1 = 'https://www.futbin.com/22/playerGraph?type=today&year=22&player=151227355&set_id=120'
url2 = 'https://www.futbin.com/22/player/303/zinedine-zidane'
url3 = 'https://www.futbin.com/22/player/593/keylor-navas'
url4 = "https://api.scrapingrobot.com/?responseType=json&waitUntil=load&noScripts=false&noImages=true&noFonts=true&noCss=true&token=ba65d1b6-d1e0-4668-84fc-5c049f61ccaf"
url5 = 'https://www.chefkoch.de'
url6 = 'https://www.futbin.com/'
scraper = cloudscraper.CloudScraper()
scraper.trust_env = False


http = urllib3.PoolManager(

    cert_reqs='CERT_REQUIRED',

    ca_certs=certifi.where()

)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
    "Accept": "application/json"
           }

proxies = {
    'http': 'https//64.39.183.52:8080',
    'https': 'https://64.39.183.52:8080'
           }


def get_data(source):
    req, gateway = helper(source)
    if req.status_code == 403:
        print(req.status_code)
        gateway.shutdown()
        #get_data(source)
        return req


def helper(source):
    gateway = ApiGateway(source)
    gateway.start()
    scraper.mount(source, gateway)
    #cookies = dict(scraper.cookies)
    req = scraper.get(source)
    gateway.shutdown()
    return req


def fetch_price(player_data):
    soup = BeautifulSoup(player_data.text, 'html.parser')
    player_id = soup.find('div', {'id': 'page-info'}).get('data-player-resource')

    today_hourly_url = f'https://www.futbin.com/22/playerGraph?type=today&year=22&player={player_id}&set_id='
    yesterday_hourly_url = f'https://www.futbin.com/22/playerGraph?type=yesterday&year=22&player={player_id}&set_id='
    da_yesterday_hourly_url = f'https://www.futbin.com/22/playerGraph?type=da_yesterday&year=22&player={player_id}&set_id='

    urls = [today_hourly_url, yesterday_hourly_url, da_yesterday_hourly_url]
    prices = []

    for url in urls:
        time.sleep(random.randint(0, 3))
        d = get_data(url)
        jsn = d.json()
        prices.append(jsn)
    return prices


#return_value = [{'ps': [[1639440000000, 27688], [1639443600000, 27600], [1639447200000, 27450], [1639450800000, 27300], [1639454400000, 27100], [1639458000000, 27400], [1639461600000, 26900], [1639465200000, 26950], [1639468800000, 26850], [1639472400000, 26750], [1639476000000, 27000], [1639479600000, 26938], [1639483200000, 27000], [1639486800000, 26938], [1639490400000, 27100], [1639494000000, 27313], [1639497600000, 27150], [1639501200000, 27417], [1639504800000, 27063]], 'xbox': [[1639440000000, 26563], [1639443600000, 26700], [1639447200000, 26313], [1639450800000, 26300], [1639454400000, 26200], [1639458000000, 26750], [1639461600000, 26850], [1639465200000, 26813], [1639468800000, 26417], [1639472400000, 25813], [1639476000000, 25750], [1639479600000, 26063], [1639483200000, 26313], [1639486800000, 25938], [1639490400000, 26500], [1639494000000, 26438], [1639497600000, 26625], [1639501200000, 26813], [1639504800000, 25875]], 'pc': [[1639440000000, 28625], [1639443600000, 28000], [1639447200000, 27875], [1639450800000, 28000], [1639454400000, 27875], [1639458000000, 27375], [1639461600000, 27750], [1639465200000, 28000], [1639468800000, 26875], [1639472400000, 28250], [1639476000000, 26750], [1639479600000, 28000], [1639483200000, 28250], [1639486800000, 27750], [1639490400000, 27250], [1639494000000, 28250], [1639497600000, 28000], [1639501200000, 28500], [1639504800000, 28000]]}, {'ps': [[1639353600000, 28083], [1639357200000, 27938], [1639360800000, 27958], [1639364400000, 27800], [1639368000000, 27600], [1639371600000, 27625], [1639375200000, 27650], [1639378800000, 27750], [1639382400000, 27792], [1639386000000, 27688], [1639389600000, 27600], [1639393200000, 27950], [1639396800000, 27900], [1639400400000, 27700], [1639404000000, 27750], [1639407600000, 27688], [1639411200000, 27850], [1639414800000, 28188], [1639418400000, 27688], [1639422000000, 28000], [1639425600000, 27750], [1639429200000, 27500], [1639432800000, 27900], [1639436400000, 27500]], 'xbox': [[1639353600000, 26708], [1639357200000, 26875], [1639360800000, 27550], [1639364400000, 27700], [1639368000000, 27050], [1639371600000, 27000], [1639375200000, 26900], [1639378800000, 26850], [1639382400000, 26688], [1639386000000, 26625], [1639389600000, 26750], [1639393200000, 26375], [1639396800000, 26063], [1639400400000, 26313], [1639404000000, 27063], [1639407600000, 26875], [1639411200000, 26500], [1639414800000, 26875], [1639418400000, 26500], [1639422000000, 27333], [1639425600000, 26750], [1639429200000, 25875], [1639432800000, 26375], [1639436400000, 26563]], 'pc': [[1639353600000, 27625], [1639357200000, 27750], [1639360800000, 27750], [1639364400000, 28500], [1639368000000, 28000], [1639371600000, 28000], [1639375200000, 27500], [1639378800000, 27500], [1639382400000, 27375], [1639386000000, 27625], [1639389600000, 27750], [1639393200000, 27750], [1639396800000, 27875], [1639400400000, 28000], [1639404000000, 28250], [1639407600000, 29000], [1639411200000, 29250], [1639414800000, 27750], [1639418400000, 28500], [1639422000000, 28625], [1639425600000, 28500], [1639429200000, 28250], [1639432800000, 27625], [1639436400000, 27500]]}, {'ps': [[1639267200000, 23375], [1639270800000, 23500], [1639274400000, 23300], [1639278000000, 23375], [1639281600000, 24063], [1639285200000, 23700], [1639288800000, 23800], [1639292400000, 23750], [1639296000000, 23250], [1639299600000, 23063], [1639303200000, 23650], [1639306800000, 23900], [1639310400000, 24125], [1639314000000, 23950], [1639317600000, 24250], [1639321200000, 24313], [1639324800000, 24313], [1639328400000, 24417], [1639332000000, 26958], [1639335600000, 27667], [1639339200000, 27625], [1639342800000, 28150], [1639346400000, 27938], [1639350000000, 27950]], 'xbox': [[1639267200000, 21250], [1639270800000, 21875], [1639274400000, 21875], [1639278000000, 22050], [1639281600000, 22000], [1639285200000, 22625], [1639288800000, 22100], [1639292400000, 22100], [1639296000000, 22050], [1639299600000, 22125], [1639303200000, 21375], [1639306800000, 21563], [1639310400000, 22500], [1639314000000, 22375], [1639317600000, 22625], [1639321200000, 22417], [1639324800000, 23833], [1639328400000, 23313], [1639332000000, 26700], [1639335600000, 27350], [1639339200000, 26950], [1639342800000, 27200], [1639346400000, 26833], [1639350000000, 26438]], 'pc': [[1639267200000, 23000], [1639270800000, 23625], [1639274400000, 23875], [1639278000000, 24750], [1639281600000, 24500], [1639285200000, 24750], [1639288800000, 25000], [1639292400000, 24250], [1639296000000, 24333], [1639299600000, 24500], [1639303200000, 24375], [1639306800000, 23750], [1639310400000, 24000], [1639314000000, 23625], [1639317600000, 24250], [1639321200000, 23750], [1639324800000, 24500], [1639328400000, 25000], [1639332000000, 28375], [1639335600000, 28000], [1639339200000, 27250], [1639342800000, 27625], [1639346400000, 28125], [1639350000000, 28250]]}]

def get_min_max(data_set):
    ps = []
    for days in data_set:
        ps.append(days['ps'])

    smallest = [ps[0][0], ps[1][0], ps[2][0]]
    greatest = [ps[0][0], ps[1][0], ps[2][0]]
    i = 0
    for days in ps:
        for values in days:
            if values[1] < smallest[i][1]:
                smallest[i] = values
            if values[1] > greatest[i][1]:
                greatest[i] = values
        i += 1
    return smallest, greatest


def compute_difference(smallest, greatest):
    difference = []
    i = 0
    for smaller in smallest:
        greater = greatest[i]
        difference.append(greater[1] - smaller[1])
    return difference


#player = helper(url2)
#soup = BeautifulSoup(player.text, 'html.parser')
#print(soup)
#print(player.status_code)
#if player.status_code == 200:
#    print("done")
#    data = fetch_price(player)
#    print(data)
#    s, g = get_min_max(data)
#    diff = compute_difference(s, g)
#    print(s)
#    print(g)
#    print(diff)
#else:
#    print(player.text)
#    print("Captcha triggered")

def return_header():
    ua = UserAgent()
    chrome = ua.chrome
    splitted = chrome.split('/')
    version = splitted[3][:2]
    header = {
        'authority': 'www.futbin.com',
        'method': 'GET',
        'path': '/22/players?page=1&ps_price=0-5000&version=gold',
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

send_proxies = "45.128.220.132:59394"

urls = [
        "https://www.futbin.com/players?page=1&ps_price=0-5000&version=gold",
        "https://www.futbin.com/players?page=2&ps_price=0-5000&version=gold",
        "https://www.futbin.com/players?page=3&ps_price=0-5000&version=gold",
        "https://www.futbin.com/players?page=4&ps_price=0-5000&version=gold",
        "https://www.futbin.com/players?page=5&ps_price=0-5000&version=gold",
        "https://www.futbin.com/players?page=6&ps_price=0-5000&version=gold",
        "https://www.futbin.com/players?page=7&ps_price=0-5000&version=gold",
        "https://www.futbin.com/players?page=8&ps_price=0-5000&version=gold",
        "https://www.futbin.com/players?page=9&ps_price=0-5000&version=gold",
        "https://www.futbin.com/players?page=10&ps_price=0-5000&version=gold",
        "https://www.futbin.com/players?page=11&ps_price=0-5000&version=gold",
        "https://www.futbin.com/players?page=12&ps_price=0-5000&version=gold",
        "https://www.futbin.com/players?page=13&ps_price=0-5000&version=gold",
        "https://www.futbin.com/players?page=14&ps_price=0-5000&version=gold",
        "https://www.futbin.com/players?page=15&ps_price=0-5000&version=gold",
        "https://www.futbin.com/players?page=16&ps_price=0-5000&version=gold",
        "https://www.futbin.com/players?page=17&ps_price=0-5000&version=gold",
        "https://www.futbin.com/players?page=18&ps_price=0-5000&version=gold",
        "https://www.futbin.com/players?page=19&ps_price=0-5000&version=gold",
        "https://www.futbin.com/players?page=20&ps_price=0-5000&version=gold",
        "https://www.futbin.com/players?page=21&ps_price=0-5000&version=gold",
        "https://www.futbin.com/players?page=22&ps_price=0-5000&version=gold",
        "https://www.futbin.com/players?page=23&ps_price=0-5000&version=gold",
        "https://www.futbin.com/players?page=24&ps_price=0-5000&version=gold",
        "https://www.futbin.com/players?page=25&ps_price=0-5000&version=gold",
        "https://www.futbin.com/players?page=26&ps_price=0-5000&version=gold",
        "https://www.futbin.com/players?page=27&ps_price=0-5000&version=gold",
        "https://www.futbin.com/players?page=28&ps_price=0-5000&version=gold",
        "https://www.futbin.com/players?page=29&ps_price=0-5000&version=gold",
        "https://www.futbin.com/players?page=30&ps_price=0-5000&version=gold",
        "https://www.futbin.com/players?page=31&ps_price=0-5000&version=gold",
        "https://www.futbin.com/players?page=32&ps_price=0-5000&version=gold",
        "https://www.futbin.com/players?page=33&ps_price=0-5000&version=gold",
        "https://www.futbin.com/players?page=34&ps_price=0-5000&version=gold",
        "https://www.futbin.com/players?page=35&ps_price=0-5000&version=gold",
        "https://www.futbin.com/players?page=36&ps_price=0-5000&version=gold",
        "https://www.futbin.com/players?page=37&ps_price=0-5000&version=gold",
        "https://www.futbin.com/players?page=38&ps_price=0-5000&version=gold",
        "https://www.futbin.com/players?page=39&ps_price=0-5000&version=gold",
        "https://www.futbin.com/players?page=40&ps_price=0-5000&version=gold",
        "https://www.futbin.com/players?page=41&ps_price=0-5000&version=gold",
        "https://www.futbin.com/players?page=42&ps_price=0-5000&version=gold",
        "https://www.futbin.com/players?page=43&ps_price=0-5000&version=gold",
        "https://www.futbin.com/players?page=44&ps_price=0-5000&version=gold",
        "https://www.futbin.com/players?page=45&ps_price=0-5000&version=gold",
        "https://www.futbin.com/players?page=46&ps_price=0-5000&version=gold",
        "https://www.futbin.com/players?page=47&ps_price=0-5000&version=gold",
        "https://www.futbin.com/players?page=48&ps_price=0-5000&version=gold",
        "https://www.futbin.com/players?page=49&ps_price=0-5000&version=gold",
        "https://www.futbin.com/players?page=50&ps_price=0-5000&version=gold",
        "https://www.futbin.com/players?page=51&ps_price=0-5000&version=gold",
        "https://www.futbin.com/players?page=52&ps_price=0-5000&version=gold",
        "https://www.futbin.com/players?page=53&ps_price=0-5000&version=gold",
        "https://www.futbin.com/players?page=54&ps_price=0-5000&version=gold",
        "https://www.futbin.com/players?page=55&ps_price=0-5000&version=gold",
        "https://www.futbin.com/players?page=56&ps_price=0-5000&version=gold",
        "https://www.futbin.com/players?page=57&ps_price=0-5000&version=gold"
    ]

fetched = []


def fetch(url, gate):
    try:
        header = return_header()
        ua = header['user-agent']
        scraper1 = cloudscraper.create_scraper(interpreter='nodejs', delay=10)
        scraper1.trust_env = False
        scraper1.mount(url6, gate)
        with scraper1.get(url, timeout=15, headers=header) as response:
            if response.status_code == 200:
                print('Gottcha')
                urls.remove(url)
                fetched.append(url)
                return response
            else:
                print('Captcha')
                return '0'
    except Exception as E:
        print(E)
        return '0'


#used = 0
#gate = ApiGateway(url6)
#gate.start()
#for url1 in urls:
#    if used <= 5:
#        fetch(url1, gate)
#        used += 1
#    else:
#        gate.shutdown()
#        used = 0
#        gate = ApiGateway(url6)
#        gate.start()
#        fetch(url1, gate)

url = 'https://www.futbin.com/players?page=1'
headers1 = {'Authority': 'www.futbin.com',
'Method': 'GET',
'Path': '/players?page=1',
'Scheme': 'https',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'es-ES,es;q=0.9',
'Cache-Control': 'max-age=0',
'Cookie': 'pc=true; ps=true; xbox=true; cookieconsent_status=dismiss; PHPSESSID=4ijtnhr6vacmjp1ppg9e57q280; theme_player=true; comments=true; platform=ps4',
'Referer': 'https://www.futbin.com/',
'Sec-CH-UA': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
'Sec-CH-UA-Mobile': '?0',
'Sec-CH-UA-Platform': '"Windows"',
'Sec-Fetch-Dest': 'document',
'Sec-Fetch-Mode': 'navigate',
'Sec-Fetch-Site': 'same-origin',
'Sec-Fetch-User': '?1',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}

gate = ApiGateway(url6)
gate.start()
scraper = cloudscraper.CloudScraper(delay=10)
scraper.trust_env = False
scraper.mount(url6, gate)
r = scraper.get(url, timeout=10, headers=headers1)
while r.status_code != 200:
    if r.status_code == 200:
        print(r.cookies.get_dict())
    else:
        r = scraper.get(url, timeout=10, headers=headers1)
        time.sleep(1)
        print('c')
if r.status_code == 200:
    print(r.cookies.get_dict())

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

