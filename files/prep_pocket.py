#/usr/bin/env python2
import glob
import json
import os
from pprint import pprint


def parse_data(files):
    for file in files:
        with open(file) as data_file:    
            data  =  json.load(data_file)
        output_log = open(file.replace(".json",".log"), 'w')
        error_log = open (file.replace(".json",".err"),'w')
        total_cnt = 0
        miss_resolved_id = 0

        for v in data['list'].itervalues():
            try:
                del v['image']
            except KeyError:
                pass
            try:
                del v['images']
            except KeyError:
                pass
            try:
                del v['videos']
            except KeyError:
                pass
            if v.get('resolved_id'):
                if v['resolved_id'] == 0:
                    # print "Resolved Id is 0"
                    miss_resolved_id += 1
                    error_log.write(json.dumps(v) + '\n')        
                    continue    
            else:
                # print "No Resolved Id"
                miss_resolved_id += 1
                error_log.write(json.dumps(v) + '\n')        
                continue

            if v.get('authors'):
                try:
                    author_data = v['authors'].values()
                    v['authors'] = [(i['name'].encode('utf-8')) for i in author_data]
                except BaseException:
                    print v['authors']
            if v.get('tags'):
                try:
                    tag_data = v['tags'].values()
                    v['tags'] = [a.encode('utf-8') for a in v['tags'].keys()]            
                except BaseException:
                    print  v['tags']   
            new_json  =  (json.dumps(v))
            output_log.write(new_json + '\n')
            total_cnt += 1
        print "Total",file,total_cnt
        print "Missing Resolved Id",file, miss_resolved_id


def main():
    path = './data/raw/'
    files = glob.glob('./' + path + '/*.json')
    parse_data(files)

main()


