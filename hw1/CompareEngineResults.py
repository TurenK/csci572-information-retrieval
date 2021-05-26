from bs4 import BeautifulSoup
import time
import requests
from random import randint
import json
import re
import csv
import os
import random
import pandas as pd
from numpy import *

USER_AGENT = [
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
    "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
    "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
	"Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25",
]
SEARCHING_URL1 = 'https://search.yahoo.com/search?p='
SEARCHING_URL2 = '&n=30'
QUERY_SET = '100QueriesSet2.txt'
GOOGLE_RESULT = 'Google_Result2.json'
CSV_HEAD = ['Queries', 'Number of Overlapping Results', 'Percent Overlap', 'Spearman Coefficient']
JSON_PATH = 'hw1.json'
CSV_PATH = 'hw1.csv'


def search(query, sleep=True):
    if sleep:  # Prevents loading too many pages too soon
        time.sleep(randint(10, 20))
    temp_url = '+'.join(query.split())  # for adding + between words for the query
    url = SEARCHING_URL1 + temp_url + SEARCHING_URL2
    soup = BeautifulSoup(requests.get(url, headers={'User-Agent': random.choice(USER_AGENT)}).text, "html.parser")
    new_results = scrape_search_result(soup)
    return new_results


def scrape_search_result(soup):
    raw_results = soup.find_all('a', class_='ac-algo fz-l ac-21th lh-24')
    results = []
    # implement a check to get only 10 results and also check that URLs must not be duplicated
    for result in raw_results:
        link = washLink(result.get('href'))
        if len(results) > 0 and link in results:
            continue
        results.append(link)
        if len(results) >= 10:
            break
    return results


def washLink(link):
    temp = re.findall(r'RU=(.*?)/RK=', link)
    if len(temp) <= 0:
        return link
    temp = re.sub(r'%2f', '/', temp[0])
    temp = re.sub(r'%3a', ':', temp)
    return temp


def readTxt(path):
    with open(path, 'r') as f:
        data = []
        for line in f.readlines():
            data.append(line.strip())
    return data


def readJson(path):
    with open(path, 'r') as f:
        data = json.load(f)
    return data


def writetojson(path, data):
    with open(path, 'a+') as f:
        json.dump(data, f)


def writecsvhead(path):
    with open(path, 'w') as f:
        csv_write = csv.writer(f)
        csv_write.writerow(CSV_HEAD)


def writetocsv(path, data):
    with open(path, 'a+') as f:
        csv_write = csv.writer(f)
        csv_write.writerows(data)


def calculate(new_result, google_result):
    after_clear_google = []
    for raw_result in google_result:
        temp_result = re.sub(r'^https://www\.|^http://www\.|^http://|^https://|^www\.', '',
                             raw_result.strip().strip('/')).lower()
        after_clear_google.append(temp_result)

    after_clear_new = []
    rank_new = []
    rank_google = []
    num_overlapping = 0
    sum_di_square = 0
    for i in range(len(new_result)):
        temp_result = re.sub(r'^https://www\.|^http://www\.|^http://|^https://|^www\.', '',
                             new_result[i].strip().strip('/')).lower()
        if len(after_clear_new) > 0 and temp_result in after_clear_new:
            continue
        after_clear_new.append(temp_result)
        if temp_result not in after_clear_google:
            continue
        rank_new.append(i)
        num = after_clear_google.index(temp_result)
        rank_google.append(num)
        num_overlapping += 1
        sum_di_square += pow(num - i, 2)

    percent_overlap = num_overlapping / len(google_result) * 100

    if num_overlapping <= 0:
        rho = 0.0
    elif num_overlapping == 1:
        rho = 1.0 if rank_new[0] == rank_google[0] else 0.0
    else:
        rho = 1.0 - 6.0 * sum_di_square / (num_overlapping * (pow(num_overlapping, 2) - 1))

    return num_overlapping, percent_overlap, rho


def main_method():
    query_set = readTxt(QUERY_SET)
    google_results = readJson(GOOGLE_RESULT)
    print(CSV_HEAD[0] + ', ' + CSV_HEAD[1] + ', ' + CSV_HEAD[2] + ', ' + CSV_HEAD[3])
    if not os.path.exists(CSV_PATH):
        writecsvhead(CSV_PATH)
    result_json = {}
    result_csv = []
    tag = False
    for i in range(0, len(query_set)):
        query = query_set[i]
        query_num_str = 'Query ' + str(i + 1)
        google_result = list(google_results.values())[i]
        new_result = search(query, sleep=True)
        k = 0
        while len(new_result) <= 0:
            new_result = search(query, sleep=False)
            k += 1
            if k > 4:
                break
        if len(new_result) <= 0:
            print('IP blocked')
            print('now i is ' + str(i))
            writetojson(JSON_PATH, result_json)
            writetocsv(CSV_PATH, result_csv)
            tag = True
            break
        result_json[query] = new_result
        num_overlapping, percent_overlap, rho = calculate(new_result, google_result)
        result_csv.append([query_num_str, num_overlapping, percent_overlap, rho])
        print(query_num_str + ', ' + str(num_overlapping) + ', ' + str(percent_overlap) + ', ' + str(round(rho, 4)))
    if not tag:
        writetojson(JSON_PATH, result_json)
        writetocsv(CSV_PATH, result_csv)


def readcsv(path):
    csv_data = pd.read_csv(CSV_PATH)
    num_overlap = csv_data['Number of Overlapping Results']
    percent_overlap = csv_data['Percent Overlap']
    rho = csv_data['Spearman Coefficient']
    return num_overlap, percent_overlap, rho

def calculate_average():
    num_overlap, percent_overlap, rho = readcsv(CSV_PATH)
    writetocsv(CSV_PATH, [['Averages', mean(num_overlap), mean(percent_overlap), mean(rho)]])


if __name__ == '__main__':
    #main_method()
    calculate_average()
    # result_json = {'a':['a','aa','aaa'], 'b': ['a','aa','aaa']}
    # result_csv = [['Query 1', 5, 50.0, -3.45],['Query 2', 5, 50.0, -3.45],['Query 3', 5, 50.0, -3.45]]
    # writetojson(JSON_PATH, result_json)
    # writetocsv(CSV_PATH, result_csv)
