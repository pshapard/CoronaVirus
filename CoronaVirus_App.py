#Author: Patrick Shapard
#Created: 03/27/2020
#Updated: 03/31/2020
#This script is used to calulate the mortality rate of the corona virus for a country or worldwide

import time
import sys
import logging
from coronavirus import ClassesFuncs
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import sys
import requests
from bs4 import BeautifulSoup

print(f'Version of class module {ClassesFuncs.__version__}')
print(f'Author of class module {ClassesFuncs.__author__}')


filename = 'CoronaVirus_Calc'
TimeStamp = time.strftime("%m_%d_%Y")
#outputFile = 'debug_script.txt'
outputFile = 'TestResults.txt'

#print(help(str))
#print(help(str))

def islength(var1):
    count = len(var1)
    if 39 <= count <= 40:
        return (var1[25:32])
    elif 38 <= count <= 39:
        return (var1[25:31])
    elif 41 <= count <= 44:
        return (var1[25:34])
    elif 20 <= count <= 21:
        return (var1[6:13])
    elif 19 <= count <= 20:
        return (var1[6:12])
    elif 18 <= count <= 19:
        return (var1[6:11])
    elif 17 <= count <= 18:
        return (var1[6:10])
    elif 16 <= count <= 17:
        return (var1[6:9])

def Get_data_per_country(url_link, country):
    stats = []
    URL = url_link
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all(class_="maincounter-number")
    for i in results:
        var1 = (i.contents[1])
        var1 = list(i)
        var1 = (str(var1[1]))
        var1 = var1.replace(",","")
        var1 = islength(var1)
        stats.append(var1)

    for idx, value in enumerate(stats):
        if idx == 0:
            total_cases = value
        elif idx == 1:
            total_deaths = value
        elif idx == 2:
            total_recover = value
    try:
        return int(total_cases) , int(total_deaths)
    except ValueError:
        print("The variable is not an integer")


def AnalyzeCoronaVirus(country):
    if country == 'world':
        url_link = 'https://www.worldometers.info/coronavirus/'
        num_cases, num_deaths = Get_data_per_country(url_link, country)
    else:
        url_link = 'https://www.worldometers.info/coronavirus/country/{}/' .format(country)
        num_cases, num_deaths = Get_data_per_country(url_link, country)
    return country, num_cases, num_deaths

def CalcTheRate( num_cases, num_deaths):
    rate_obj = ClassesFuncs.CalcMortalRate(num_cases, num_deaths)
    virus_rate_raw = (rate_obj.calc())
    virus_rate = (format(virus_rate_raw, '.2f'))
    return virus_rate

def CreateFile(virus_rate, country, num_cases, num_deaths):
    with open(outputFile, 'a') as f:
        f.write("\n{}: {}: Total cases: {}, Total deaths: {}, Death rate: {}%" .format(TimeStamp, country, num_cases, num_deaths, virus_rate))
        logging.info("{}: Total cases: {}, Total deaths: {}, Death rate: {}%" .format(country, num_cases, num_deaths, virus_rate))



def main():
    ClassesFuncs.setup_logging_Enhanced(filename)
    list_of_country = ['world','us','italy','france','iran','uk','germany','spain']
    for country in list_of_country:
        country, num_cases, num_deaths= AnalyzeCoronaVirus(country)
        virus_rate= CalcTheRate(num_cases, num_deaths)
        CreateFile(virus_rate, country.capitalize(), num_cases, num_deaths)




if __name__ == '__main__':
    main()
