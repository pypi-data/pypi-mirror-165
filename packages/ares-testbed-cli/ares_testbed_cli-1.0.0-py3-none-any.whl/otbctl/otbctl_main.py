from multiprocessing import context
import sys, getopt
import os
import argparse        
import dotenv 
from .log_management import log_management

class otbcli():

    def __init__(self, name):
        self.name = name

    def init(self):
        infoDualLogger = log_management.get_info_dual_logger()
        infoDualLogger.info('name is {}'.format(self.name))
  
    def setContext(context):
        env_file = f"{os.path.expanduser('~')}/.otbctl/.env"

        if os.path.exists(env_file):
            print(env_file)
            f = open(env_file,'w')
            env_context = 'otbctl-context='+context
            f.write(env_context)
            f.close()
        
    def getContext(current):
        env_file = f"{os.path.expanduser('~')}/.otbctl/.env"

        if os.path.exists(env_file):
            dotenv.load_dotenv(env_file, override=True)
            return os.environ.get(current)

        else:
            return 'Context not found'