#Created: 03/27/2020
#Updated: 04/03/2020
#Module for corona virus classes and functions

import sys
import logging
import time

__version__ = '1.03'
__author__ = 'Patrick R. Shapard'

class CalcMortalRate(object):
    """Class object to calculate corona virus death rate in %. """
    def __init__(self, num_cases, num_deaths):
        self.num_cases = num_cases
        self.num_deaths = num_deaths
    
    def calc(self):
        """Function calculates the corona virus death rate. """
        try:
            return ((self.num_deaths/self.num_cases)*100)
        except ZeroDivisionError:
            logging.error("Function attempted to devide by zero")
            sys.exit(0)


def create_log_file(filename, level=logging.DEBUG):
    """Function creates log files and is used in setup_logging_Enhanced(file). """
    TimeStamp = time.strftime("%Y%m%d_%H%M%S")
    handler = logging.FileHandler(filename)
    handler.setLevel(level)
    formatter = logging.Formatter('%(asctime)s %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    handler.setFormatter(formatter)
    logging.getLogger('').addHandler(handler)


def setup_logging_Enhanced(file):
    """Function setups logging function with 4 logging levels:
       DEBUG, WARNING, ERROR, INFO. """
    #components = ('_' + enc + '_' + version + '_' + carbon_fw)
    components = ('_' + file)
    logging.getLogger('').setLevel(logging.DEBUG)
    TimeStamp = time.strftime("%Y%m%d_%H%M%S")
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)
    #open up a few files for logging at different levels
    create_log_file('logs/' + TimeStamp + components + '_DEBUG.log', logging.DEBUG)
    create_log_file('logs/' + TimeStamp + components + '_INFO.log', logging.INFO)
    create_log_file('logs/' + TimeStamp + components + '_WARNING.log', logging.WARNING)
    create_log_file('logs/' + TimeStamp + components + '_ERROR.log', logging.ERROR)
    #create_log_file('logs/' + TimeStamp + components + '_CRITICAL.log', logging.CRITICAL)
    #create_log_file('logs/' + TimeStamp + components + '_TESTCASES.log', logging.TESTCASES)
    #logging.basicConfig() 
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True

def countdown(t):
    """Timer function, receives 1 variable in seconds """
    while t:
        mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        t -= 1
    print('Goodbye!\n\n\n\n\n')
