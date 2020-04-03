#Created: 03/27/2020
#Updated: 03/27/2020
#Module for corona virus classes and functions

import sys
import logging
import time

__version__ = '1.03'
__author__ = 'Patrick R. Shapard'

class CalcMortalRate(object):
    
    def __init__(self, num_cases, num_deaths):
        self.num_cases = num_cases
        self.num_deaths = num_deaths
    
    def calc(self):
        try:
            return ((self.num_deaths/self.num_cases)*100)
        except ZeroDivisionError:
            logging.error("Function attempted to devide by zero")
            sys.exit(0)


def create_log_file(filename, level=logging.DEBUG):
    TimeStamp = time.strftime("%Y%m%d_%H%M%S")
    handler = logging.FileHandler(filename)
    handler.setLevel(level)
    formatter = logging.Formatter('%(asctime)s %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    handler.setFormatter(formatter)
    logging.getLogger('').addHandler(handler)


def setup_logging_Enhanced(file):
    #Set up logging
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