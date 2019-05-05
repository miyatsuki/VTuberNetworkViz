import numpy as np
import csv
from sklearn import manifold
import math
import sys

channel_list = []
outlier_channel_list = []

channel_id_name_map = {}
with open('../data/channels_2434.tsv', "r", encoding='utf-8') as f:
    tsv = csv.reader(f, delimiter='\t')
    for row in tsv:
        channel_name = row[0]
        channel_id = row[1]
        if channel_id not in outlier_channel_list:
            channel_list.append(channel_id)
            channel_id_name_map[channel_id] = channel_name

channel_id_image_url_map = {}
with open('../data/playlist_2434.tsv', "r", encoding='utf-8') as f:
    tsv = csv.reader(f, delimiter='\t')
    for row in tsv:
        channel_name = row[0]
        channel_id = row[1]
        playlist_id = row[2]
        channel_image_url = row[3]

        if channel_id not in outlier_channel_list:
            channel_id_image_url_map[channel_id] = channel_image_url

collab_channel_set = set()
with open('../data/collab_list_2434.tsv', "r", encoding='utf-8') as f:
    tsv = csv.reader(f, delimiter='\t')
    for row in tsv:
        base_channel_id = row[1]
        collab_channel_id = row[3]

        if collab_channel_id == "":
            continue

        if base_channel_id in channel_list and collab_channel_id in channel_list:
            collab_channel_set.add(base_channel_id)
            collab_channel_set.add(collab_channel_id)


video_collab_map = {}
with open('../data/collab_list_2434.tsv', "r", encoding='utf-8') as f:
    tsv = csv.reader(f, delimiter='\t')
    for row in tsv:
        base_channel_id = row[1]
        video_id = row[2]
        collab_channel_id = row[3]

        if collab_channel_id == "":
            continue

        if video_id not in video_collab_map:
            video_collab_map[video_id] = set()

        if base_channel_id in collab_channel_set and collab_channel_id in collab_channel_set:
            video_collab_map[video_id].add(base_channel_id)
            video_collab_map[video_id].add(collab_channel_id)

collab_channel_list = list(collab_channel_set)
collab_times_mat = np.zeros((len(collab_channel_list), len(collab_channel_list)))
for channel_id_set in video_collab_map.values():
    collab_list = list(channel_id_set)
    for i in range(len(collab_list)):
        for j in range(i, len(collab_list)):
            base_channel_id_index = collab_channel_list.index(collab_list[i])
            collab_channel_id_index = collab_channel_list.index(collab_list[j])
            collab_times_mat[base_channel_id_index, collab_channel_id_index] += 1
            collab_times_mat[collab_channel_id_index, base_channel_id_index] += 1

# 1/(コラボ回数) = 距離とする
dist_mat = np.zeros((len(collab_channel_list), len(collab_channel_list)))
for i in range(collab_times_mat.shape[0]):
    for j in range(collab_times_mat.shape[0]):
        if i == j:
            dist_mat[i, j] = 0
        #elif collab_times_mat[i, j] > 0:
        #    dist_mat[i, j] = 1/collab_times_mat[i, j]
        else:
            dist_mat[i, j] = max(collab_times_mat.shape[0] - collab_times_mat[i, j]*4, 0)


"""
for k in range(dist_mat.shape[0]):
    for i in range(dist_mat.shape[0]):
        for j in range(dist_mat.shape[0]):
            if dist_mat[i, j] > (dist_mat[i, k] + dist_mat[k, j]):
                dist_mat[i, j] = dist_mat[i, k] + dist_mat[k, j]
"""

print("start mds")
mds = manifold.MDS(n_components=2, dissimilarity="precomputed", random_state=6)
vtuber_plot = mds.fit_transform(dist_mat)
print("end mds")

for i in range(vtuber_plot.shape[0]):
    for j in range(vtuber_plot.shape[1]):
        vtuber_plot[i, j] = np.sign(vtuber_plot[i, j]) * abs(vtuber_plot[i, j]) ** (1.2)

abs_max = 0
for row in vtuber_plot:
    for i in range(len(row)):
        if abs(row[i]) > abs_max:
            abs_max = abs(row[i])
scale = 0.95/abs_max
vtuber_plot *= scale

for row in vtuber_plot:
    print(str(row[0]) + "\t" + str(row[1]))


np.savetxt('../data/distmat.tsv', dist_mat)
with open('../view/plot_data.js', "w", encoding='utf-8') as f:
    f.write("plot_data = [" + "\n")
    for i, index in enumerate(collab_channel_list):
        f.write("{" + 'id:"' + str(index) + '"'
                + ', name:"' + channel_id_name_map[index]
                + '", posX:' + str(vtuber_plot[i, 0])
                + ", posY:" + str(vtuber_plot[i, 1]) 
                + ', url:"' + channel_id_image_url_map[index] + '"'
                + "}")

        if i < len(collab_channel_list) - 1:
            f.write(",\n")
        else:
            f.write("]")
    
    f.write("\n\n")

    # distmat
    f.write("collab_times_mat = [")
    row_count = 0
    for row in collab_times_mat:
        f.write('[')
        f.write(','.join(map(str, row.tolist())))
        f.write(']')

        
        row_count += 1
        if row_count < len(dist_mat):
            f.write(',\n')
        else:
            f.write("]")
