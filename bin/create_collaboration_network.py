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

class VideoInfo:
    def __init__(self, video_info_json):
        self.video_id = video_info_json["id"]
        self.channel_id = video_info_json["snippet"]["channelId"]
        self.publish_time = video_info_json["snippet"]["publishedAt"]
        self.description = video_info_json["snippet"]["description"]
        self.collaborate_set = self.get_collab_channel_list(self.description)

    def get_collab_channel_list(self, description):
        ans = set()

        url_regex = r'((http|https)://www\.youtube\.com/channel/((\w|\-|_)+))'
        m = re.findall(url_regex, description)


        for found_list in m:
            collab_id = found_list[2]

            # 自分のチャンネルだったら飛ばす
            if self.channel_id == collab_id:
                continue

            # typo? とかでinvalidなid拾うことがあるのでチェック
            if len(collab_id) == 24:
                ans.add(collab_id)

        return ans

    def __str__(self):
        info = [self.video_id, self.channel_id, self.publish_time, str(self.collaborate_set)]
        return "\t".join(info)


bin_dir=os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.normpath(os.path.join(bin_dir, '../data/'))
video_dir = os.path.normpath(os.path.join(bin_dir, '../video/'))
base_dir = os.path.normpath(os.path.join(bin_dir, '../'))

# 取得した動画情報から必要な部分だけ取り出す
p = Path(base_dir + "/video/")
video_info_list = []
for video_path in p.glob("*.json"):
    with open(video_path) as f:
        try:
            video_info = VideoInfo(json.load(f))
            video_info_list.append(video_info)
        except Exception:
            continue


# コラボ情報を縦持ちのファイルにして出力
with open(base_dir + '/data/network.tsv', 'w') as f:
    for video_info in video_info_list:
        if len(video_info.collaborate_set) > 0:
            for collab in video_info.collaborate_set:
                info = [video_info.channel_id, video_info.video_id, video_info.publish_time, collab]
                f.write("\t".join(info) + "\n")
        else:
            info = [video_info.channel_id, video_info.video_id, video_info.publish_time]
            f.write("\t".join(info) + "\n")

