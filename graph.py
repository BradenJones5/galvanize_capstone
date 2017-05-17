import pandas as pd
import numpy as np
from get_data import get_data
import networkx as nx
from scalers import scale_data_total_passatt
from sklearn.metrics import pairwise_distances
import matplotlib.pyplot as plt


def create_graph(matrix):
    '''
    input: a 2d numpy similarity matrix
    output: a graph based on the similarity between qbs
    '''

    rows, cols = np.where(matrix >= .925)
    edges = zip(rows.tolist(), cols.tolist())
    edges = [(x,y) for x,y in edges if not x ==y]
    gr = nx.Graph()
    gr.add_edges_from(edges)

    nx.draw_networkx(gr, node_color = 'tomato', font_color = 'white', edge_color = 'cadetblue',
                        width= 2.0, font_family = 'arial', linewidths = 2.0, alpha = .9)

    plt.axis("off")
    plt.show()

if __name__ == '__main__':
    data = get_data('all_seasons.csv')
    data = data[data['year'] == 2016]
    X = scale_data_total_passatt(data)
    mat = 1- pairwise_distances(X, metric='l1')
    create_graph(mat)
