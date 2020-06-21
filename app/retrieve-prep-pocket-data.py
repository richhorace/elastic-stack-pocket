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
    parser = argparse.ArgumentParser(description='Pass Epoch time for since.')    
    parser.add_argument('--e', metavar='epoch', type=str, help='epoch value without milliseconds') 
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
            logging.error('"pocket_data": {}, "filename": {}'.format(json.dumps(v)))
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
    if args.e is not None:
        since_epoch = args.e
    else:
        print('Epoch value not passed, will process previous day')
        previous_day = (date.today() - timedelta(days=1))
        previous_day = previous_day.timetuple()
        since_epoch = str(time.mktime(previous_day))

    fname = since_epoch + '-data.json'
    data = get_data(since_epoch,fname)
    parse_data(data,fname)

main()