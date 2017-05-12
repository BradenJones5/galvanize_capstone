import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from get_data import get_data
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score


subset_df, feature_matrix = get_data('2016_season.csv')

pca = PCA(n_components = 2)
pca.fit_transform(feature_matrix)
pca_2d = pca.transform(feature_matrix)


subset_df['pca_x'] = pd.Series(pca_2d[:,0], index = subset_df.index)
subset_df['pca_y'] = pd.Series(pca_2d[:,1], index = subset_df.index)

for n_clusters in range(2, 9):
    kmeans = KMeans(n_clusters = n_clusters)
    cluster_labels = kmeans.fit_predict(feature_matrix)
    silhouette_avg = silhouette_score(feature_matrix, cluster_labels)
    print "for {} clusters, the avg silhouette_score is: {}".format(n_clusters, silhouette_avg)

kmeans = KMeans(n_clusters = 4)
kmeans.fit(feature_matrix)

cluster_labels = kmeans.labels_
subset_df['Cluster Group'] = pd.Series(cluster_labels, index = subset_df.index)


plt.scatter(subset_df['pca_x'].values, subset_df['pca_y'].values, c = subset_df['Cluster Group'].values)
plt.suptitle('QB clusters for the 2016 season')
plt.xlabel('PCA_1')
plt.ylabel('PCA_2')
plt.savefig('base_cluster.png')
plt.show()
