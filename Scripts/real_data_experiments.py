from time import time
from graph_manager.plot_tools import *
from graph_manager.dataset_manager import *
from dendrogram_manager.plot_tools import *
from dendrogram_manager.homogeneous_cut_slicer import *
from dendrogram_manager.heterogeneous_cut_slicer import *
from dendrogram_manager.cluster_cut_slicer import *
from dendrogram_manager.distance_slicer import *
from clustering_algorithms.louvain import *
from clustering_algorithms.paris import *
from experiments.results_manager import save_clusters

DISPLAY_PLOTS = False
SAVE_PLOTS = False
SAVE_RESULTS = True
directory_datasets = "/home/sharp/Documents/Graphs/Graph_Clustering/Datasets/"
# dataset_name = "openflight_clean"
# dataset_name = "openstreet_clean"
# dataset_name = "soccer_players_clean"
# dataset_name = "dico_clean"
# dataset_name = "hum-wikipedia_clean"
dataset_name = "dblp_clean"
# dataset_name = "openflight"
# dataset_name = "openstreet"
# dataset_name = "soccer_players"
# dataset_name = "dico"
# dataset_name = "hum-wikipedia"
# dataset_name = "dblp"
directory_results = "/home/sharp/Documents/Graphs/Graph_Clustering/Results/"
results_file_name = dataset_name
n_results = 8

### Clean dataset and extract the largest connected component
# G, pos, label = load_dataset(directory_datasets, dataset_name)
# G, pos, label = clean_dataset(G, pos, label)
# G, pos, label = extract_dataset_connected_components(G, pos, label)
# G, pos, label = clean_dataset(G, pos, label)
# save_dataset(directory_datasets, dataset_name + "_clean", G, pos, label)

### Load dataset
G, pos, label = load_dataset(directory_datasets, dataset_name)

### Display information about the dataset
print(nx.info(G))
if DISPLAY_PLOTS and pos != {}:
    plot_graph(G, pos)

### Apply Paris
time_paris = time()
D = paris(G)
time_paris = time() - time_paris
print("Paris", time_paris)

print("Best clusters")
ranked_cuts, ranked_scores = ranking_cluster_cuts(D, lambda w, x, y:  (np.log(x)-np.log(y)))
for i in range(n_results):
    print(i, ranked_scores[i])
    C = [clustering_from_cluster_cut(D, ranked_cuts[i])]
    if DISPLAY_PLOTS and pos != {}:
        plot_graph_clustering(G, C, pos)
        # plot_dendrogram_clustering(D, C)
    if SAVE_PLOTS and pos != {}:
        plot_graph_clustering(G, C, pos, file_name=results_file_name + "_clusters_graph" + str(i))
        # plot_dendrogram_clustering(D, C, file_name=results_file_name + "_clusters_dendrogram" + str(i))
    if SAVE_RESULTS and label != {}:
        save_clusters(C, label, directory_results, results_file_name + "_clusters" + str(i))

print("Best homogeneous cuts")
ranked_cuts, ranked_scores = ranking_homogeneous_cuts(D, lambda w, x, y: w * (np.log(x)-np.log(y)))
ranked_cuts, ranked_scores = filter_homogeneous_ranking(ranked_cuts, ranked_scores, D, threshold=.1)
for i in range(n_results):
    print(i, ranked_scores[i])
    C = clustering_from_homogeneous_cut(D, ranked_cuts[i])
    if DISPLAY_PLOTS and pos != {}:
        plot_graph_clustering(G, C, pos)
        # plot_dendrogram_clustering(D, C)
    if SAVE_PLOTS and pos != {}:
        plot_graph_clustering(G, C, pos, file_name=results_file_name + "_homogeneous_graph" + str(i))
        # plot_dendrogram_clustering(D, C, file_name=results_file_name + "_homogeneous_dendrogram" + str(i))
    if SAVE_RESULTS and label != {}:
        save_clusters(C, label, directory_results, results_file_name + "_homogeneous" + str(i))

print("Best heterogeneous cuts")
ranked_cuts, ranked_scores = ranking_heterogeneous_cuts(D, n_results, lambda w, x, y: w * (np.log(x)-np.log(y)))
for i in range(n_results):
    print(i, ranked_scores[i])
    C = clustering_from_heterogeneous_cut(D, ranked_cuts[i])
    if DISPLAY_PLOTS and pos != {}:
        plot_graph_clustering(G, C, pos)
        # plot_dendrogram_clustering(D, C)
    if SAVE_PLOTS and pos != {}:
        plot_graph_clustering(G, C, pos, file_name=results_file_name + "_heterogeneous_graph" + str(i))
        # plot_dendrogram_clustering(D, C, file_name=results_file_name + "_heterogeneous_dendrogram" + str(i))
    if SAVE_RESULTS and label != {}:
        save_clusters(C, label, directory_results, results_file_name + "_heterogeneous" + str(i))

# print("Best resolutions")
# ranked_distances, ranked_scores = ranking_distances(D, lambda w, x, y: w * (np.log(x)-np.log(y)))
# ranked_distances, ranked_scores = filter_distance_ranking(ranked_distances, ranked_scores, D, threshold=.1)
# for i in range(n_results):
#     print(i, ranked_scores[i], 1/ranked_distances[i])
#     C = louvain(G, 1/float(ranked_distances[i]))
#     if DISPLAY_PLOTS and pos != {}:
#         plot_graph_clustering(G, C, pos)
#         # plot_dendrogram_clustering(D, C)
#     if SAVE_PLOTS and pos != {}:
#         plot_graph_clustering(G, C, pos, file_name=results_file_name + "_resolution_graph" + str(i))
#         # plot_dendrogram_clustering(D, C, file_name=results_file_name + "_resolution_dendrogram" + str(i))
#     if SAVE_RESULTS and label != {}:
#         save_clusters(C, label, directory_results, results_file_name + "_resolution" + str(i))
