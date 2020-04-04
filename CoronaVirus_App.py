#Author: Patrick Shapard
#Created: 03/27/2020
#Updated: 04/03/2020
#This script is used to calulate the mortality rate of the corona virus for a country or worldwide
#The data is pulled from 

import time
import sys
import logging
from coronavirus import ClassesFuncs
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import requests
from bs4 import BeautifulSoup

print(f'Version of class module {ClassesFuncs.__version__}')
print(f'Author of class module {ClassesFuncs.__author__}')


file_name = 'CoronaVirus_Calc'
TimeStamp = time.strftime("%Y_%m_%d_%H%M%S")
#outputFile = 'debug_script.txt'
outputFile = 'TestResults.txt'


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

def OutPutToCountryLog():
    filename = 'TestResults.txt'
    
    output_file = {'World':'logfile_world.txt',
                   'Us':'logfile_usa.txt',
                   'France':'logfile_france.txt',
                   'Spain':'logfile_spain.txt',
                   'Germany':'logfile_germany.txt',
                   'Uk':'logfile_uk.txt',
                   'Iran':'logfile_iran.txt',
                   'Italy':'logfile_italy.txt'}
    
    for string, logfile in output_file.items():
        with open(filename) as outf:
            datafile = outf.readlines()
            string_found = [line for line in datafile if string in line]
            with open(logfile, 'w') as inf:
                for line in string_found:
                    inf.write(line)

def main():
    ClassesFuncs.setup_logging_Enhanced(file_name)
    list_of_country = ['world','us','italy','france','iran','uk','germany','spain']
    while True:
        for country in list_of_country:
            country, num_cases, num_deaths= AnalyzeCoronaVirus(country)
            virus_rate= CalcTheRate(num_cases, num_deaths)
            CreateFile(virus_rate, country.capitalize(), num_cases, num_deaths)

        OutPutToCountryLog()
        logging.info("Pausing 60 mins before fetching new data")
        ClassesFuncs.countdown(3600)



if __name__ == '__main__':
    main()
