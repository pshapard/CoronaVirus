# Author: Patrick Shapard
# Created: 03/27/2020
# Updated: 04/04/2020
# This script is used to calculate the mortality rate of the corona virus for a country or worldwide
# The data is pulled from https://www.worldometers.info website

import time
import logging
from coronavirus.ClassesFuncs import CalcRate
from coronavirus.ClassesFuncs import setup_logging_Enhanced
from coronavirus.ClassesFuncs import countdown
from bs4 import BeautifulSoup
import requests

file_name = 'CoronaVirus_App'
outputFile = 'TestResults.txt'


def islength(var1):
    """Function to check the variable length of the Total cases,
       total death cases and total recovered cases."""
    count = len(var1)
    if 39 <= count <= 40:
        return var1[25:32]
    elif 38 <= count <= 39:
        return var1[25:31]
    elif 41 <= count <= 44:
        return var1[25:34]
    elif 20 <= count <= 21:
        return var1[6:13]
    elif 19 <= count <= 20:
        return var1[6:12]
    elif 18 <= count <= 19:
        return var1[6:11]
    elif 17 <= count <= 18:
        return var1[6:10]
    elif 16 <= count <= 17:
        return var1[6:9]


def Get_data_per_country(url_link):
    """Parses the data from url_link and returns three variables """
    stats = []
    URL = url_link
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all(class_="maincounter-number")
    for i in results:
        var1 = (i.contents[1])
        var1 = list(i)
        var1 = (str(var1[1]))
        var1 = var1.replace(",", "")
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
        return int(total_cases), int(total_deaths), int(total_recover)
    except ValueError:
        print("The variable is not an integer")


def AnalyzeCoronaVirus(country):
    """Connects to the url and downloads the data and returns
       value for country, total cases and death cases.  """
    if country == 'world':
        url_link = 'https://www.worldometers.info/coronavirus/'
        num_cases, num_deaths, num_recover = Get_data_per_country(
            url_link)
    else:
        url_link = 'https://www.worldometers.info/coronavirus/country/{}/' .format(
            country)
        num_cases, num_deaths, num_recover = Get_data_per_country(
            url_link)
    return country, num_cases, num_deaths, num_recover


def CalcTheRate(num_cases, num_deaths, num_recover):
    """Receives three variables. calculates and returns the death and recover rates. """
    rate_obj = CalcRate(num_cases, num_deaths, num_recover)
    death_rate_raw = (rate_obj.death())
    recover_rate_raw = (rate_obj.recover())
    death_rate = (format(death_rate_raw, '.2f'))
    recover_rate = (format(recover_rate_raw, '.2f'))
    return death_rate, recover_rate


def CreateFile(death_rate, recover_rate, country, num_cases, num_deaths, num_recover):
    """Receives 6 variables.  Opens main log file and writes the variables in each country log"""
    TimeStamp = time.strftime("%m/%d/%Y_%H:%M:%S")
    with open(outputFile, 'a') as f:
        f.write(f"\n{TimeStamp}: {country}: Total cases: {num_cases}, Total deaths: {num_deaths}, Total Reovered: {num_recover}, Death rate: {death_rate}%, Recovery Rate: {recover_rate}%")
        logging.info(f"{country}: Total cases: {num_cases}, Total deaths: {num_deaths}, Total recovered: {num_recover}, Death rate: {death_rate}%, Recovery Rate: {recover_rate}%")


def OutPutToCountryLog():
    """Open and reads main log file, TestResults.txt
       Searches main log file for country string and 
       retrieves data for each country and outputs 
       the data to each country's log file """
    filename = 'TestResults.txt'
    output_file = {'World': 'logfile_world.txt',
                   'Us': 'logfile_usa.txt',
                   'France': 'logfile_france.txt',
                   'Spain': 'logfile_spain.txt',
                   'Germany': 'logfile_germany.txt',
                   'Uk': 'logfile_uk.txt',
                   'Iran': 'logfile_iran.txt',
                   'Italy': 'logfile_italy.txt'}

    for string, logfile in output_file.items():
        with open(filename) as outf:
            datafile = outf.readlines()
            string_found = [line for line in datafile if string in line]
            with open(logfile, 'w') as inf:
                for line in string_found:
                    inf.write(line)


def main():
    count = 0
    setup_logging_Enhanced(file_name)
    list_of_country = ['world', 'us', 'italy',
                       'france', 'iran', 'uk', 'germany', 'spain']
    while count <= 10000:
        logging.info(f'Number of iterations: {count}')
        for country in list_of_country:
            country, num_cases, num_deaths, num_recover = AnalyzeCoronaVirus(
                country)
            death_rate, recover_rate = CalcTheRate(
                num_cases, num_deaths, num_recover)
            CreateFile(death_rate, recover_rate, country.capitalize(),
                       num_cases, num_deaths, num_recover)

        OutPutToCountryLog()
        logging.info("Pausing 3 hours before fetching new data")
        countdown(10800)
        count += 1


if __name__ == '__main__':
    main()
