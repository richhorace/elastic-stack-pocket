import argparse
import config
from datetime import date, timedelta
import time
import glob
import json
import logging
import requests

from local import DATA_DIR, LOG_DIR

LOG_PATH = '{}/getpocket.log'.format(LOG_DIR)

consumer_key = config.consumer_key
access_token = config.access_token

logging.basicConfig(level=logging.INFO,
                    format='{"retrieved": "%(asctime)s", "level": "%(levelname)s", %(message)s}',
                    filename=LOG_PATH,
                    filemode='a+')

def parse_args():
    """
    Parse command line args
    """
    parser = argparse.ArgumentParser(description='Pass number of days back to start from')    
    parser.add_argument('-d', '--days_back',dest='days_back', type=int, default=1, help='Number of days back') 
    return parser.parse_args()


def get_data(since_epoch,fname):
    headers = {
        'Content-Type': 'application/json',
        'X-Accept': 'application/json',
    }

    data = '{"consumer_key":"' + consumer_key + '","access_token":"' + access_token + '","state":"all", "detailType":"complete", "sort":"oldest", "since":"' + since_epoch + '"}'
    # print(data)

    response = requests.post('https://getpocket.com/v3/get', headers=headers, data=data, verify=False)

    data = response.json()
    with open(DATA_DIR + fname, 'w') as f:
        json.dump(data, f)
    f.close()
    
    return data

def parse_data(data,fname):
    total = 0
    resolved_id_missing = 0

    for v in data['list'].values():
        fn = {"filename": fname }        
        v.update(fn)
        # Remove unnecessary data
        if v.get('image'):
            del v['image']
        if v.get('images'):
            del v['images']
        if v.get('videos'):
            del v['videos']

        if v.get('resolved_id', 0) == 0:
            resolved_id_missing += 1
            logging.error('"pocket_data": {}'.format(json.dumps(v)))
            continue

        if v.get('authors'):
            try:
                author_data = v['authors'].values()
                v['authors'] = [(a['name']) for a in author_data]
            except BaseException:
                print(v['authors'])

        if v.get('tags'):
            try:
                tag_data = v['tags'].keys()
                v['tags'] = [a for a in tag_data]
            except BaseException:
                print(v['tags'])

        fn = {"filename": fname }        
        v.update(fn)
        logging.info('"pocket_data": {}'.format(json.dumps(v)))
        total += 1

    print("Total ({}): {}".format(fname, total))
    print("Missing Resolved Id ({}): {}".format(fname, resolved_id_missing))


def main():
    args = parse_args()
    num_days = args.days_back
    start_date = (date.today() - timedelta(days=num_days))
    start_date = start_date.timetuple()
    since_epoch = str(round(time.mktime(start_date)))
    fname = since_epoch + '-data.json'
    data = get_data(since_epoch,fname)
    parse_data(data,fname)

main()