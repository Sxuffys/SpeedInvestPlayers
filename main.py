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
import requests_html
from urllib3 import Retry
from requests.adapters import HTTPAdapter
import undetected_chromedriver as uc
from selenium import webdriver


url1 = 'https://www.futbin.com/22/playerGraph?type=today&year=22&player=151227355&set_id=120'
url2 = 'https://www.futbin.com/22/player/303/zinedine-zidane'
url3 = 'https://www.futbin.com/22/player/593/keylor-navas'
url4 = "https://api.scrapingrobot.com/?responseType=json&waitUntil=load&noScripts=false&noImages=true&noFonts=true&noCss=true&token=ba65d1b6-d1e0-4668-84fc-5c049f61ccaf"
url5 = 'https://www.chefkoch.de'
url6 = 'https://www.futbin.com/'
scraper = cloudscraper.CloudScraper()

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
    if req.status_code != 200:
        print(req.status_code)
        gateway.shutdown()
        get_data(source)
    return req


def helper(source):
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    driver = uc.Chrome(options=options)
    gateway = ApiGateway(source)
    gateway.start()
    driver.mount(source, gateway)
    #cookies = dict(scraper.cookies)
    req = driver.get(source, proxies=proxies)
    return req, gateway


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


player = get_data(url2)
print(player.status_code)
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

send_header = {
               'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux armv7l; rv:17.0) Gecko/20100101 Firefox/17.0'}

send_proxies = "45.128.220.132:59394"

url = 'https://github.com/corbanworks/aws-blocker'



#gateway = ApiGateway(url1)
#gateway.start()
## Assign gateway to session
#session = requests.session()
##adapter = session.get_adapter(url=url1)
##session.cert
#
#
#scraper.mount(url1, gateway)
cookies = dict(scraper.cookies)
##print(cookies)
#user = UserAgent()
#
## Send request (IP will be randomised)
#response = scraper.get(url1, headers=headers)
#print(response.status_code)
##print(response.text)

# Delete gateways
#gateway.shutdown()