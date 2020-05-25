#/usr/bin/env python3

import glob
import json
import logging

from local import DATA_DIR, LOG_PATH


logging.basicConfig(level=logging.INFO,
                    format='{"timestamp": "%(asctime)s", "level": "%(levelname)s", %(message)s}',
                    filename=LOG_PATH,
                    filemode='a+')


def parse_files(fnames):
    for fname in fnames:
        data = read_file(fname)
        parse_data(data, fname)


def read_file(fname):
    with open(fname, 'r', encoding='utf-8') as f:
        return json.load(f)


def parse_data(data, fname=None):
    total = 0
    resolved_id_missing = 0

    for v in data['list'].values():
        # Remove unnecessary data
        if v.get('image'):
            del v['image']
        if v.get('images'):
            del v['images']
        if v.get('videos'):
            del v['videos']

        if v.get('resolved_id', 0) == 0:
            resolved_id_missing += 1
            logging.error('"message": {}, "filename": {}'.format(json.dumps(v), fname))
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
        logging.info('"message": {}'.format(json.dumps(v)))
        total += 1

    print("Total ({}): {}".format(fname, total))
    print("Missing Resolved Id ({}): {}".format(fname, resolved_id_missing))


def main():
    # Get local JSON file names
    file_names = glob.glob('{}/*.json'.format(DATA_DIR))
    # Parse all JSON files
    parse_files(file_names)


main()


