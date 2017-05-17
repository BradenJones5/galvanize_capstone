import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from get_data import get_data
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import AgglomerativeClustering
from scalers import scale_data_total_passatt, get_scaled_feature_matrix

def plot_pca_clusters(pca_x, pca_y, labels):
    '''
    input: numpy array of 1st principal components (x-axis)
           numpy array of 2nd principla components (y-axis)
           numpy array of the cluster group labels
    output: plot displaying the clustered data
    '''
    plt.scatter(pca_x, pca_y, c = labels)
    plt.suptitle('QB clusters for the 2016 season')
    plt.xlabel('PCA_1')
    plt.ylabel('PCA_2')
    plt.savefig('base_cluster.png')
    plt.show()


subset_df = get_data('all_seasons.csv')
# subset_df = subset_df[subset_df['year'] >= 2015]
scaler = StandardScaler()
X = scaler.fit_transform(subset_df.iloc[:,2:13:2].values)
X_1 = scale_data_total_passatt(subset_df)
X_2 = get_scaled_feature_matrix(subset_df)

def plot_player_trend(list_of_players, dataframe):
    '''
    input: a list of players to plot
    output:
    '''

for n_clusters in range(2, 9):
    for X in [X, X_1, X_2]:
        kmeans = KMeans(n_clusters = n_clusters)
        wards = AgglomerativeClustering(n_clusters = n_clusters, linkage = 'complete')
        cluster_labels = kmeans.fit_predict(X)
        cluster_labels_ward = wards.fit_predict(X)
        silhouette_avg = silhouette_score(X, cluster_labels)
        silhouette_avg_wards = silhouette_score(X, cluster_labels_ward)
        print "for {} clusters, the avg silhouette_score is: {}".format(n_clusters, silhouette_avg)
        print "for {} clusters, the avg silhouette_score is: {}".format(n_clusters, silhouette_avg_wards)

pca = PCA(n_components = 2)
pca.fit_transform(X_1)
pca_2d = pca.transform(X_1)
subset_df['pca_x'] = pd.Series(pca_2d[:,0], index = subset_df.index)
subset_df['pca_y'] = pd.Series(pca_2d[:,1], index = subset_df.index)

kmeans = KMeans(n_clusters = 4, init='k-means++')
kmeans.fit_transform(X_1)

cluster_labels = kmeans.labels_
subset_df['Cluster Group'] = pd.Series(cluster_labels, index = subset_df.index)

plt.scatter(subset_df['pca_x'].values, subset_df['pca_y'].values, c = subset_df['Cluster Group'].values)
