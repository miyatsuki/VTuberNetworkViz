import numpy as np
import csv
import sys
import networkx as nx
import datetime
import os

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

channel_list = []
channel_id_name_map = {}
channel_id_debut_map = {}
with open('../settings/channels_2434.tsv', "r", encoding='utf-8') as f:
    tsv = csv.reader(f, delimiter='\t')
    for row in tsv:
        channel_name = row[0]
        channel_id = row[1]
        debut_type = row[2]

        channel_list.append(channel_id)
        channel_id_name_map[channel_id] = channel_name
        channel_id_debut_map[channel_name] = debut_type

channel_id_image_url_map = {}
#with open('../data/playlist_2434.tsv', "r", encoding='utf-8') as f:
#    tsv = csv.reader(f, delimiter='\t')
#    for row in tsv:
#        channel_name = row[0]
#        channel_id = row[1]
#        playlist_id = row[2]
#        channel_image_url = row[3]

#        channel_id_image_url_map[channel_id] = channel_image_url

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
channel_list = []
previous_pos_map = {}

while counter_ut <= end_ut:
    datetime_jst = str(datetime.datetime.fromtimestamp(counter_ut))
    print(datetime_jst)

    included_node_list = []

    for node in collabNode_list:
        if node.published_at <= counter_ut:
            included_node_list.append(node)
            if node.from_channel not in channel_list:
                channel_list.append(node.from_channel)
            if node.to_channel is not None and node.to_channel not in channel_list:
                channel_list.append(node.to_channel)

    collab_times_mat = np.zeros((len(channel_list), len(channel_list)))
    for node in included_node_list:
        if node.to_channel is None:
            continue

        # TODO: コラボ人数に基づく正規化
        base_channel_id_index = channel_list.index(node.from_channel)
        collab_channel_id_index = channel_list.index(node.to_channel)
        collab_times_mat[base_channel_id_index, collab_channel_id_index] += 1
        collab_times_mat[collab_channel_id_index, base_channel_id_index] += 1

    max_collab_times = np.max(collab_times_mat)

    # コラボ回数を重みとする
    G = nx.Graph()
    for i in range(collab_times_mat.shape[0]):
        G.add_node(i)
        for j in range(collab_times_mat.shape[0]):
            if i < j and collab_times_mat[i, j] > 0:
                G.add_edge(i, j, weight=collab_times_mat[i, j])

    np.random.seed(0)
    for i in range(len(channel_list)):
        if i not in previous_pos_map:
            previous_pos_map[i] = np.random.rand(1, 2)[0]/100.0

    spring_pos = nx.spring_layout(G, seed=6, pos=previous_pos_map)

    for i in range(len(channel_list)):
        previous_pos_map[i] = spring_pos[i]

    date_jst = datetime_jst.split(" ")[0].replace("-", "")
    with open(data_dir + "/pos/" + date_jst + ".tsv", "w") as f:
        for i in range(len(channel_list)):
            f.write(str(i) + "\t" + str(previous_pos_map[i][0]) + "\t" + str(previous_pos_map[i][1]) + "\n")

    counter_ut += 3600 * 24
