# -*- coding: utf-8 -*-

import requests
import csv
import json
from time import sleep
import sys
import re

channel_url = 'https://www.googleapis.com/youtube/v3/channels'
playlist_url = 'https://www.googleapis.com/youtube/v3/playlistItems'
video_url = 'https://www.googleapis.com/youtube/v3/videos'

# this file is not shared with github
# create own secrets.json like
#{
#    "youtube_dataAPI_token": "YOUR API TOKEN"
#}
with open('../secrets.json', "r") as f:
    secrets = json.load(f)

# channel -> playlist
with open('../data/channels_2434.tsv', "r", encoding='utf-8') as fr:
    with open('../data/playlist_2434.tsv', "w", encoding='utf-8') as fw:
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
with open('../data/playlist_2434.tsv', "r", encoding='utf-8') as fr:
    with open('../data/video_list_2434.tsv', "w", encoding='utf-8') as fw:
        tsv = csv.reader(fr, delimiter='\t')

        for row in tsv:
            pageToken = ""
            while True:
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
                    sleep(1)
                    continue

                id_list = []
                for i in range(len(playlist_result["items"])):
                    video_id = playlist_result["items"][i]["contentDetails"]["videoId"]
                    publishedAt = playlist_result["items"][i]["snippet"]["publishedAt"]

                    fw.write(channel_name + "\t" + channel_id + "\t" + video_id + "\t" + publishedAt + "\n")
                    print(channel_name + "\t" + channel_id + "\t" + video_id + "\t" + publishedAt)
                        
                sleep(1)

                # 残りのアイテム数がmaxResultsを超えている場合はnextPageTokenが帰ってくる
                if "nextPageToken" in playlist_result:
                    pageToken = playlist_result["nextPageToken"]
                else:
                    break

# videolist -> collab_list
exist_video_set = set()
with open('../data/collab_list_2434.tsv', "r", encoding='utf-8') as fr:
    tsv = csv.reader(fr, delimiter='\t')

    for row in tsv:
        channel_name = row[0]
        channel_id = row[1]
        video_id = row[2]
        collab_channel_id = row[3]
        exist_video_set.add(video_id)

new_video_id_list = []
with open('../data/video_list_2434.tsv', "r", encoding='utf-8') as fr:
    tsv = csv.reader(fr, delimiter='\t')

    for row in tsv:
        video_id = row[2]
        if video_id not in exist_video_set:
            new_video_id_list.append(video_id)

with open('../data/collab_list_2434.tsv', "a", encoding='utf-8') as fw:
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
        for i in range(len(video_list_result["items"])):
            url_regex = r'((http|https)://www\.youtube\.com/channel/((\w|\-|_)+))'
            m = re.findall(url_regex, video_list_result["items"][i]["snippet"]["description"])

            video_id = video_list_result["items"][i]["id"]
            channel_name = video_list_result["items"][i]["snippet"]["channelTitle"]
            channel_id = video_list_result["items"][i]["snippet"]["channelId"]

            collab_id_list = []
            for str_tup in m:
                collab_id = str_tup[2]

                # 自分のチャンネルだったら飛ばす
                if channel_id == collab_id:
                    continue

                # typo? とかでinvalidなid拾うことがあるのでチェック
                if len(collab_id) == 24:
                    collab_id_list.append(collab_id)

            if len(collab_id_list) > 0:
                for collab_id in collab_id_list:
                    fw.write(channel_name + "\t" + channel_id + "\t" + video_id + "\t" + collab_id + "\n")
                    print(channel_name + "\t" + channel_id + "\t" + video_id + "\t" + collab_id)
                    
            else:
                fw.write(channel_name + "\t" + channel_id + "\t" + video_id + "\t" + "" + "\n")
                print(channel_name + "\t" + channel_id + "\t" + video_id + "\t" + "")

        sleep(1)
