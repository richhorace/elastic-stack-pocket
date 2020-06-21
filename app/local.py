#/usr/bin/env python3
import os

DATA_DIR = '../data/raw/'
LOG_DIR = '../data/logs'
REPROCESS_DIR = '../data/reprocess'


paths = [DATA_DIR,LOG_DIR,REPROCESS_DIR]

for path in paths:
    if not os.path.exists(path):
        os.makedirs(path)