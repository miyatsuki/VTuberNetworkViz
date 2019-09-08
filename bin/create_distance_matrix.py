import numpy as np
import csv
from sklearn import manifold
import math
import sys
import networkx as nx

channel_list = []

channel_id_name_map = {}
channel_id_debut_map = {}
with open('../data/channels_2434.tsv', "r", encoding='utf-8') as f:
    tsv = csv.reader(f, delimiter='\t')
    for row in tsv:
        channel_name = row[0]
        channel_id = row[1]
        debut_type = row[2]

        channel_list.append(channel_id)
        channel_id_name_map[channel_id] = channel_name
        channel_id_debut_map[channel_name] = debut_type

channel_id_image_url_map = {}
with open('../data/playlist_2434.tsv', "r", encoding='utf-8') as f:
    tsv = csv.reader(f, delimiter='\t')
    for row in tsv:
        channel_name = row[0]
        channel_id = row[1]
        playlist_id = row[2]
        channel_image_url = row[3]

        channel_id_image_url_map[channel_id] = channel_image_url

video_collab_map = {}
with open('../data/collab_list_2434.tsv', "r", encoding='utf-8') as f:
    tsv = csv.reader(f, delimiter='\t')
    for row in tsv:
        base_channel_id = row[1]
        video_id = row[2]
        collab_channel_id = row[3]

        if video_id not in video_collab_map:
            video_collab_map[video_id] = set()

        video_collab_map[video_id].add(base_channel_id)

        if collab_channel_id in channel_id_name_map:
            video_collab_map[video_id].add(collab_channel_id)

collab_channel_list = list(channel_id_name_map.keys())
collab_times_mat = np.zeros((len(collab_channel_list), len(collab_channel_list)))
for channel_id_set in video_collab_map.values():
    collab_list = list(channel_id_set)
    for i in range(len(collab_list)):
        for j in range(i, len(collab_list)):
            base_channel_id_index = collab_channel_list.index(collab_list[i])
            collab_channel_id_index = collab_channel_list.index(collab_list[j])
            collab_times_mat[base_channel_id_index, collab_channel_id_index] += 1/len(channel_id_set)
            collab_times_mat[collab_channel_id_index, base_channel_id_index] += 1/len(channel_id_set)

# 1/(コラボ回数) = 距離とする
G = nx.Graph()
dist_mat = np.zeros((len(collab_channel_list), len(collab_channel_list)))
for i in range(collab_times_mat.shape[0]):
    G.add_node(i)
    for j in range(collab_times_mat.shape[0]):
        if i == j:
            dist_mat[i, j] = 0
        #elif collab_times_mat[i, j] > 0:
        #    dist_mat[i, j] = 1/collab_times_mat[i, j]
        else:
        #    dist_mat[i, j] = 1
        #    dist_mat[i, j] = max(collab_times_mat.shape[0] - collab_times_mat[i, j]*4, 0)
            dist_mat[i, j] = max(10 - collab_times_mat[i, j], 0)
            if i < j:
                G.add_edge(i, j, weight=collab_times_mat[i, j])

spring_pos = nx.spring_layout(G, seed=6)
print(spring_pos)

import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram
result1 = linkage(collab_times_mat, method = 'median')
                  #metric = 'braycurtis', 
                  #metric = 'canberra', 
                  #metric = 'chebyshev', 
                  #metric = 'cityblock', 
                  #metric = 'correlation', 
                  #metric = 'cosine', 
                  #metric = 'euclidean', 
                  #metric = 'hamming', 
                  #metric = 'jaccard', 
                  #method= 'single')
                  #method = 'ward')
                  #method= 'complete')
                  #method='weighted')

channel_name_list = [ channel_id_name_map[c] for c in channel_list]
dendrogram(result1, labels=channel_name_list, orientation='right')
plt.title("Dedrogram")
plt.ylabel("Threshold")
#plt.show()


"""
for k in range(dist_mat.shape[0]):
    for i in range(dist_mat.shape[0]):
        for j in range(dist_mat.shape[0]):
            if dist_mat[i, j] > (dist_mat[i, k] + dist_mat[k, j]):
                dist_mat[i, j] = dist_mat[i, k] + dist_mat[k, j]
"""

print("start mds")
mds = manifold.MDS(n_components=2, n_init=500, max_iter=1200, dissimilarity="precomputed", random_state=6)
vtuber_plot = mds.fit_transform(dist_mat)
print("end mds")

print(vtuber_plot)

for i in range(vtuber_plot.shape[0]):
    for j in range(vtuber_plot.shape[1]):
        print(str(i) + "\t" + str(j))
        # vtuber_plot[i, j] = np.sign(vtuber_plot[i, j]) * abs(vtuber_plot[i, j]) ** (0.9)
        vtuber_plot[i, j] =  np.sign(spring_pos[i][j]) * abs(spring_pos[i][j]) ** (1.0/4)
        
        
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

    f.write("\n\n")

    # debut_map
    f.write("debut_map = {")
    row_count = 0
    for i, index in enumerate(channel_id_debut_map.keys()):
        f.write('"' + index + '":"' + channel_id_debut_map[index] + '"')

        row_count += 1
        if row_count < len(channel_id_debut_map.keys()):
            f.write(',\n')
        else:
            f.write("}")
