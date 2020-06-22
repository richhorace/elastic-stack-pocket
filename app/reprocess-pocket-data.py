#/usr/bin/env python3
import argparse
import glob
import json
import logging
import datetime
import os

from local import DATA_DIR, LOG_DIR, REPROCESS_DIR


def parse_files(fnames):
    for fname in fnames:
        stat = os.stat(fname)
        f_date = str(datetime.datetime.utcfromtimestamp(stat.st_birthtime).isoformat())
        data = read_file(fname)
        parse_data(data, fname,f_date )


def read_file(fname):
    with open(fname, 'r', encoding='utf-8') as f:
        return json.load(f)

def parse_data(data, fname, f_date):
    LOG_PATH = '{}/getpocket-reprocessed.log'.format(LOG_DIR)

    logging.basicConfig(level=logging.INFO,
                        format='{"retrieved": "' + f_date +'", "level": "%(levelname)s", %(message)s}',
                        filename=LOG_PATH,
                        filemode='a+')

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
            # logging.error('"pocket_data": {}, "filename": {}'.format(json.dumps(v)))
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
    # Get local JSON file names
    file_names = glob.glob('{}/*.json'.format(REPROCESS_DIR))
    # Parse all JSON files
    parse_files(file_names)

main()


