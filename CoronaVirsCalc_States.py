# Author: Patrick Shapard
# Created: 04/04/2020
# Updated: 04/05/2020
# This script is used to calulate the mortality rate of the corona virus for the USA and each state
# The data is pulled from https://www.worldometers.info website


import time
import logging
import requests
from bs4 import BeautifulSoup
from coronavirus import ClassesFuncs


url_link = 'https://www.worldometers.info/coronavirus/country/us/'
outputFile = 'States_TestResults.txt'
file_name = 'WebParser_States'


def Get_data_per_state(url_link):
    """Parses the data from url_link, calculates death rate and output to state logs """
    URL = url_link
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, 'lxml')
    rows = soup.find(
        class_="table table-bordered table-hover table-responsive usa_table_countries").find_all('tr')[1:]

    for row in rows:
        cell = [i.text for i in row.find_all('td')]
        states, totals, death = cell[0], cell[1], cell[3]
        mylist = list([states, totals, death])
        for idx, value in enumerate(mylist):
            value = value.replace("\n", "")
            value = value.replace(",", "")
            value = value.replace(" ", "")
            if idx == 0:
                state = value
            elif idx == 1:
                num_cases = int(value)
            elif idx == 2:
                num_deaths = str(value)
                if num_deaths != '':
                    num_deaths = int(value)
                else:
                    num_deaths = None

        if num_deaths is not None:
            death_rate = CalcTheRate(num_cases, num_deaths)
        else:
            death_rate = None
        CreateFile(state, death_rate, num_cases, num_deaths)
        OutPutToStateLog(state)


def CalcTheRate(num_cases, num_deaths):
    """Receives three variables. calculates and returns the death and recover rates. """
    rate_obj = ClassesFuncs.CalcRate(num_cases, num_deaths)
    death_rate_raw = (rate_obj.death())
    death_rate = (format(death_rate_raw, '.2f'))
    return death_rate


def CreateFile(state, death_rate, num_cases, num_deaths):
    """Receives 4 variables.  Opens main log file and writes the variables in each state log"""
    TimeStamp = time.strftime("%m/%d/%Y_%H:%M:%S")
    with open(outputFile, 'a') as f:
        f.write(
            f"\n{TimeStamp}: {state}: Total cases: {num_cases}, Total deaths: {num_deaths}, Death rate: {death_rate}%")
        logging.info(
            f"{state}: Total cases: {num_cases}, Total deaths: {num_deaths}, Death rate: {death_rate}%")


def OutPutToStateLog(state):
    """Open and reads main log file, States_TestResults.txt
       Searches main log file and retrieves data for each state
       and outputs the data to each state's log file """
    filename = 'States_TestResults.txt'
    output_file = {state: 'c:\\Python38\\States\\logfile_' + state + '.txt'}

    for string, logfile in output_file.items():
        with open(filename) as outf:
            datafile = outf.readlines()
            string_found = [line for line in datafile if string in line]
            with open(logfile, 'w') as inf:
                for line in string_found:
                    inf.write(line)


def main():
    ClassesFuncs.setup_logging_Enhanced(file_name)
    Get_data_per_state(url_link)


if __name__ == '__main__':
    main()
