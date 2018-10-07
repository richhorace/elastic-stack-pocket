import os

DATA_DIR = './data/raw/'

LOG_DIR = 'logs'
LOG_PATH = '{}/getpocket.log'.format(LOG_DIR)

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)