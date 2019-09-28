import numpy as np
import csv
import sys
import networkx as nx
import datetime
import os
import svgwrite
import json

bin_dir=os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.normpath(os.path.join(bin_dir, '../data/'))
video_dir = os.path.normpath(os.path.join(bin_dir, '../video/'))
base_dir = os.path.normpath(os.path.join(bin_dir, '../'))

class CollabNode:
    def __init__(self, from_channel, publish_time, to_channel = None):
        self.from_channel = from_channel
        self.to_channel = to_channel
        self.published_at = self.utc_to_unixtime(publish_time) + 3600 * 9

    # フォーマットが yyyy-mm-ddTHH:MM:SS.000Z である前提
    def utc_to_unixtime(self, publish_time):
        date_string = publish_time.split("T")[0]
        time_string = publish_time.split("T")[1].split(".")[0]

        year = int(date_string.split("-")[0])
        month = int(date_string.split("-")[1])
        day = int(date_string.split("-")[2])

        hour = int(time_string.split(":")[0])
        minute = int(time_string.split(":")[1])
        second = int(time_string.split(":")[2])

        return int(datetime.datetime(year,month,day,hour,minute,second).strftime("%s"))

    def __str__(self):
        info = [self.from_channel, str(self.to_channel), str(self.published_at)]
        return "\t".join(info)

start_ut = int(sys.argv[1])
end_ut = int(sys.argv[2])

channel_id_name_map = {}
channel_id_debut_map = {}
with open('../settings/channels_2434.tsv', "r", encoding='utf-8') as f:
    tsv = csv.reader(f, delimiter='\t')
    for row in tsv:
        channel_name = row[0]
        channel_id = row[1]
        debut_type = row[2]

        channel_id_name_map[channel_id] = channel_name
        channel_id_debut_map[channel_name] = debut_type

collabNode_list = []
with open('../data/network.tsv', "r", encoding='utf-8') as f:
    tsv = csv.reader(f, delimiter='\t')
    for row in tsv:
        from_channel = row[0]
        publish_time = row[2]
        to_channel = None
        if len(row) == 4:
            to_channel = row[3]
        node = CollabNode(from_channel, publish_time, to_channel)
        collabNode_list.append(node)

counter_ut = start_ut
result_map = {}

channel_list = list(channel_id_name_map.keys())
while counter_ut <= end_ut:
    datetime_jst = str(datetime.datetime.fromtimestamp(counter_ut))
    print(datetime_jst)

    included_node_list = []
    for node in collabNode_list:
        # 30日以内の物のみカウント
        if (counter_ut - 3600*24*30) <= node.published_at <= counter_ut:
            included_node_list.append(node)

    collab_times_mat = np.zeros((len(channel_list), len(channel_list)))
    for node in included_node_list:
        if node.to_channel is None:
            continue
        if node.from_channel not in channel_list or node.to_channel not in channel_list:
            continue

        # TODO: コラボ人数に基づく正規化
        base_channel_id_index = channel_list.index(node.from_channel)
        collab_channel_id_index = channel_list.index(node.to_channel)
        collab_times_mat[base_channel_id_index, collab_channel_id_index] += 1
        collab_times_mat[collab_channel_id_index, base_channel_id_index] += 1

    result_map[counter_ut] = collab_times_mat.tolist()
    counter_ut += 3600 * 24


data = {}
data["collab_mat_list"] = result_map
data["channel_list"] = channel_list
data["channels"] = {}
with open('../data/20190922/playlist_2434.tsv', "r", encoding='utf-8') as f:
    tsv = csv.reader(f, delimiter='\t')
    for row in tsv:
        channel_id = row[1]
        data["channels"][channel_id] = {}
        data["channels"][channel_id]["name"] = channel_id_name_map[channel_id]
        data["channels"][channel_id]["image_url"] = row[3]

ut_channel_subscriber_map = {}
counter_ut = start_ut
while counter_ut <= end_ut:
    datetime_jst = str(datetime.datetime.fromtimestamp(counter_ut))
    dateYYYYMMDD = datetime_jst.split(" ")[0].replace("-", "")
    print(dateYYYYMMDD)

    channel_subscriber_map = {}
    with open('../data/' + dateYYYYMMDD + '/playlist_2434.tsv', "r", encoding='utf-8') as f:
        tsv = csv.reader(f, delimiter='\t')
        for row in tsv:
            channel_id = row[1]
            subscriber_num = int(row[4])
            channel_subscriber_map[channel_id] = subscriber_num

    ut_channel_subscriber_map[counter_ut] = []
    for i, channel_id in enumerate(channel_list):
        if channel_id in channel_subscriber_map:
            if channel_subscriber_map[channel_id] > 0:
                ut_channel_subscriber_map[counter_ut].append(channel_subscriber_map[channel_id])
            else:
                ut_channel_subscriber_map[counter_ut].append(ut_channel_subscriber_map[(counter_ut - 3600*24)][i])
        else:
            ut_channel_subscriber_map[counter_ut].append(0)

    counter_ut += 3600 * 24

data["subscriber_map"] = ut_channel_subscriber_map

with open("data.json", 'w') as f:
    json.dump(data, f, ensure_ascii=False)
