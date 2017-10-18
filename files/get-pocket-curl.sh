#!/bin/bash
access_token="Add_Access_Token"
consumer_key="Add_Consumer_Key"
since="$1"

curl https://getpocket.com/v3/get --insecure -XPOST -H "Content-Type: application/json" -H "X-Accept: application/json" -d "{\"consumer_key\":\"$consumer_key\", \"access_token\":\"$access_token\", \"state\":\"all\", \"detailType\":\"complete\", \"sort\":\"oldest\", \"since\":\"$since\"}" >./data/raw/pocket-$since.json
