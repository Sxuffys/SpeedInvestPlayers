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
from datetime import date, timedelta
import heapq
import pandas as pd


def diff_sort_key(diff):
    return diff[0]


def common_elements_players(list1, list2):
    result = []
    for element in list1:
        if element[0] in list2:
            result.append(element)
    return result

def common_elements(list1, list2):
    result = []
    unique_list = []
    for element in list1:
        for elem in list2:
            if element[0] == elem[0]:
                result.append(element)
    for x in result:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    return unique_list


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

    def compute_swings(self):
        for players in self.hourly_data['prices']:
            for day in self.hourly_data['prices'][players]:
                daily_values = []
                for value in self.hourly_data['prices'][players][day]:
                    daily_values.append(value[1])
                df = pd.DataFrame({day: daily_values})

                # Check if values are above or below a threshold
                threshold = self.min_data['min_max'][players][day][1] // 3
                if threshold > 0:
                    df['over_threshold'] = df[day] > threshold

                    # Compare to the previous row
                    # If over_threshold has changed,
                    # then you either went above or fell below the threshold
                    df['changed'] = df['over_threshold'] != df['over_threshold'].shift(1)

                    # First one has, by definition, has no previous value, so we should omit it
                    df = df.loc[1:, ]

                    # Count how many times a row is newly above or below threshold
                    counts = df.loc[df['changed']].groupby('over_threshold').agg({'changed': 'count'})
                    if len(counts.index) == 2:
                        counts.index = ["Down", "Up"]
                        counts.columns = ["Count"]
                        self.counts.append(counts)
                        print(counts, players)
                    #if len(self.min_data['min_max'][players][day]) == 3:
                    #    self.min_data['min_max'][players][day] = counts
                    #else:
                    #    for count in counts:
                    #        self.min_data['min_max'][players][day][4].update(count)

    def get_greatest_diff(self, ago):
        differences = []
        diff_with_players = []
        for players in self.min_data['min_max']:
            differences.append(self.min_data['min_max'][players][str(date.today() - timedelta(days=ago))][2])
            diff_with_players.append([self.min_data['min_max'][players][str(date.today() - timedelta(days=ago))][2], players])
        largest30 = heapq.nlargest(100, differences)
        return common_elements_players(diff_with_players, largest30)

    def get_best_player(self):
        solution = []
        for i in range(0, 3):
            solution.append(self.get_greatest_diff(i))
        return common_elements(solution[0], common_elements(solution[1], solution[2]))

    def compute_average_min(self):
        averages = []
        averages_with_players = []
        for players in self.min_data['min_max']:
            avg = 0
            for i in range(0, 3):
                avg += self.min_data['min_max'][players][str(date.today() - timedelta(days=i))][2]
            avg = avg // 3
            averages.append(avg)
            averages_with_players.append((avg, players))
        #largest30 = heapq.nlargest(10, averages)
        #largest30.sort()
        #return common_elements_players(averages_with_players, largest30)
        return averages_with_players
    
    def averages_big_diff(self, averages):
        good = []
        for avg in averages:
            diff = []
            for i in range(0, 2):
                diff.append(self.min_data['min_max'][avg[1]][str(date.today() - timedelta(days=i+1))][2])
            good_enough = True
            if avg[0] <= 1000:
                good_enough = False
            for d in diff:
                if d <= 700:
                    good_enough = False
            if good_enough:
                good.append(avg)
        return good

    def swing(self):
        for players in self.min_data['min_max']:
            for day in self.min_data['min_max'][players]:
                diff = self.min_data['min_max'][players][day][2]
                up = 0
                down = 0
                is_up = False
                is_down = True
                if diff >= 800:
                    daily_values = []
                    min = self.min_data['min_max'][players][day][0]
                    max = self.min_data['min_max'][players][day][1]
                    min_t = min + diff * 0.1
                    max_t = max - diff * 0.1
                    for value in self.hourly_data['prices'][players][day]:
                        daily_values.append(value[1])
                    for value in daily_values:
                        if (value > max_t) & is_down:
                            up += 1
                            is_up = True
                            is_down = False
                        elif (value > min_t) & is_up:
                            down += 1
                            is_down = True
                            is_up = False
                        #if value > max_t:
                        #    up += 1
                        #    is_up = True
                        #    is_down = False
                        #elif value > min_t:
                        #    down += 1
                        #    is_down = True
                        #    is_up = False
                if (up > 3) & (down > 3):
                    self.counts.append((up, down, players, day))

if __name__ == "__main__":
    pro = Price()
    pro.compute_min_max()
    time.sleep(2)
    pro.save_min_data()
    time.sleep(2)
    print(pro.get_best_player())
    avg = pro.compute_average_min()
    print(pro.averages_big_diff(avg))
    print(pro.get_greatest_diff(0))
    #print(pro.compute_swings())
    #pro.swing()
    #print(pro.counts)
    #print(pro.get_greatest_diff(1))
    #print(pro.get_greatest_diff(2))

