import json


def save_json(data, file_link='data.json'):
    with open(file_link, 'w') as outfile:
        json.dump(data, outfile, indent=4)


def creating_header():
    data = {}
    #data = json.load(open('data_header_details.json', 'r'))
    data['user_agents_links'] = [
        'https://developers.whatismybrowser.com/useragents/explore/operating_system_name/windows/',
        'https://developers.whatismybrowser.com/useragents/explore/operating_system_name/windows/2',
        'https://developers.whatismybrowser.com/useragents/explore/operating_system_name/linux/',
        'https://developers.whatismybrowser.com/useragents/explore/software_name/safari/',
        'https://developers.whatismybrowser.com/useragents/explore/software_name/opera/',
        'https://developers.whatismybrowser.com/useragents/explore/operating_system_name/chrome-os/',
        'https://developers.whatismybrowser.com/useragents/explore/hardware_type_specific/mobile/',
        'https://developers.whatismybrowser.com/useragents/explore/operating_platform_string/redmi/',
        'https://developers.whatismybrowser.com/useragents/explore/software_name/instagram/',
        'https://developers.whatismybrowser.com/useragents/explore/operating_system_name/android/',
        'https://developers.whatismybrowser.com/useragents/explore/operating_system_name/ios/',
        'https://developers.whatismybrowser.com/useragents/explore/operating_system_name/mac-os-x/'
    ]
    

    data['referrer'] = [
        "https://duckduckgo.com/",
        "https://www.google.com/",
        "http://www.bing.com/",
        "https://in.yahoo.com/",
        "https://www.azlyrics.com/",
        "https://www.dogpile.com/",
        "http://www.yippy.com",
        "https://yandex.com/"
    ]

    data['user_agents_scrap'] = []
    data['proxies'] = []
    data['working_proxies'] = []
    save_json(data, 'json_data/data_header_details.json')

def player_pager():
    data = {}
    data['not_fetched_page_urls'] = []
    for page in range(1, 58):
        data['not_fetched_page_urls'].append(f'https://www.futbin.com/players?page={page}&ps_price=0-5000&version=gold')
    data['fetched_page_urls'] = []
    data["ids_and_names"] = []
    data['player_prices'] = []
    data['player_urls'] = []
    data['player_ids'] = []
    data['player_prices'] = []
    data['not_fetched_graph_urls'] = []

    save_json(data, 'json_data/player_urls.json')

def hourly_json():
    data = {}
    data['prices'] = {}
    save_json(data, 'json_data/hourly_prices.json')

def min_json():
    data = {}
    data['min_max'] = {}
    save_json(data, 'json_data/mins_maxs.json')

def ids_json():
    data = {}
    data['ids'] = []
    save_json(data, 'json_data/player_ids.json')


if __name__ == "__main__":
    #creating_header()
    player_pager()
    hourly_json()
    ids_json()
    min_json()

