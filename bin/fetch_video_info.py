# -*- coding: utf-8 -*-

import requests
import csv
import json
from time import sleep
import sys
import re
import os
import datetime
import shutil
from pathlib import Path

bin_dir=os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.normpath(os.path.join(bin_dir, '../data/'))
video_dir = os.path.normpath(os.path.join(bin_dir, '../video/'))
base_dir = os.path.normpath(os.path.join(bin_dir, '../'))

channel_url = 'https://www.googleapis.com/youtube/v3/channels'
playlist_url = 'https://www.googleapis.com/youtube/v3/playlistItems'
video_url = 'https://www.googleapis.com/youtube/v3/videos'

# this file is not shared with github
# create own secrets.json like
#{
#    "youtube_dataAPI_token": "YOUR API TOKEN"
#}
with open(base_dir + '/settings/secrets.json', "r") as f:
    secrets = json.load(f)

yyyymmdd = datetime.date.today().strftime("%Y%m%d")
prefix = data_dir + '/' + yyyymmdd + '/'
os.mkdir(prefix)

# channel -> playlist
with open(base_dir + '/settings/channels_2434.tsv', "r", encoding='utf-8') as fr, open(prefix + '/playlist_2434.tsv', "w", encoding='utf-8') as fw:
    tsv = csv.reader(fr, delimiter='\t')

    for row in tsv:
        pageToken = ""
        channel_id = row[1]

        param = {
            'key': secrets["youtube_dataAPI_token"]
            , 'id': channel_id
            , 'part': 'snippet, contentDetails, statistics'
            , 'maxResults': '50'
            , 'pageToken': pageToken
        }

        req = requests.get(channel_url, params=param)
        channel_result = req.json()
        print(channel_result)

        if len(channel_result["items"]) > 0:
            channel_name = channel_result["items"][0]["snippet"]["title"]
            playlist_id = channel_result["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
            thumbnail_image_url = channel_result["items"][0]["snippet"]["thumbnails"]["medium"]["url"]
            subscriberCount = channel_result["items"][0]["statistics"]["subscriberCount"]

            fw.write("\t".join([channel_name, channel_id, playlist_id, thumbnail_image_url, subscriberCount]) + "\n")
            print("\t".join([channel_name, channel_id, playlist_id, thumbnail_image_url, subscriberCount]))

        sleep(1)

# playlist -> videolist
with open(prefix + '/playlist_2434.tsv', "r", encoding='utf-8') as fr, open(prefix + '/video_list_2434.tsv', "w", encoding='utf-8') as fw:
    tsv = csv.reader(fr, delimiter='\t')

    for row in tsv:
        pageToken = ""
        while True:
            sleep(1)
            channel_name = row[0]
            channel_id = row[1]
            playlist_id = row[2]
            param = {
                'key': secrets["youtube_dataAPI_token"]
                , 'playlistId': playlist_id
                , 'part': 'snippet, contentDetails'
                , 'maxResults': '50'
                , 'pageToken': pageToken
            }

            req = requests.get(playlist_url, params=param)
            playlist_result = req.json()

            # 取得失敗してたら飛ばす
            if "items" not in playlist_result:
                break

            id_list = []
            for item in playlist_result["items"]):
                video_id = item["contentDetails"]["videoId"]
                publishedAt = item["snippet"]["publishedAt"]

                fw.write(channel_name + "\t" + channel_id + "\t" + video_id + "\t" + publishedAt + "\n")
                print(channel_name + "\t" + channel_id + "\t" + video_id + "\t" + publishedAt)
                    
            # 残りのアイテム数がmaxResultsを超えている場合はnextPageTokenが帰ってくる
            if "nextPageToken" in playlist_result:
                pageToken = playlist_result["nextPageToken"]
            else:
                break

# すでに取得ずみの動画をチェック
p = Path(base_dir + "/video/")
exist_video_list = []
for video_path in p.glob("*.json"):
    video_file_name = video_path.as_posix()
    video_id = video_file_name.split("/")[-1].split(".")[0]
    exist_video_list.append(video_id)

# 取得が必要な動画のリストを作る
new_video_id_list = []
with open(prefix + '/video_list_2434.tsv', "r", encoding='utf-8') as fr:
    tsv = csv.reader(fr, delimiter='\t')

    for row in tsv:
        video_id = row[2]
        if video_id not in exist_video_list:
            new_video_id_list.append(video_id)

# 取得する動画について順番にAPIを叩いていく
for start_index in range(0, len(new_video_id_list), 50):
    end_index = min(start_index + 50, len(new_video_id_list))

    param = {
        'key': secrets["youtube_dataAPI_token"]
        , 'id': ','.join(new_video_id_list[start_index:end_index])
        , 'part': 'snippet'
    }

    req = requests.get(video_url, params=param)
    video_list_result = req.json()

    # 取得失敗してたら飛ばす
    if "items" not in video_list_result:
        sleep(1)
        continue

    id_list = []
    for i, item in enumerate(video_list_result["items"]):
        video_id = item["id"]
        with open(base_dir + "/video/" + video_id + ".json", "w", encoding='utf-8') as fw:
            fw.write(json.dumps(item, ensure_ascii=False, indent=2))

    sleep(1)
