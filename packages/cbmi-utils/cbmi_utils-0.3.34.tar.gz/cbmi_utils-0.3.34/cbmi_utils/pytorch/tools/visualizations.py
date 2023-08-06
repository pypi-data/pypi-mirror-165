from typing import Optional
import matplotlib.pyplot as plt
import numpy as np
import seaborn
import umap
from sklearn.manifold import TSNE
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler

# Depricated use plot_UMAP
# def create_umap_plot(data: np.ndarray, targets: ndnp.array = None, reducer_seed:int = 42):
#     reducer = umap.UMAP(random_state=reducer_seed)
#     mapper = reducer.fit(data)
#     umap_plot = umap.plot.points(mapper, labels=targets, theme='fire')
#     return umap_plot.figure


def create_conf_matrix_plot(data: np.ndarray, targets: np.ndarray, plot_labels='auto', normalize_matrix: str = 'all', title: str = None):
    conf_matrix = confusion_matrix(targets, data, normalize=normalize_matrix)
    conf_plot = seaborn.heatmap(
        conf_matrix,
        annot=True,
        cmap="Blues",
        xticklabels=plot_labels,
        yticklabels=plot_labels
    )

    # Layout stuff
    if title is not None:
        plt.title(f'{title}', fontsize=18)
    plt.tight_layout()

    return conf_plot.figure


def plot_UMAP(feature_vec: np.ndarray, label_vec: np.ndarray, title=None, reducer_seed: int = 42):
    # -- scale and calculate UMAP embedding
    scaled_data = StandardScaler().fit_transform(feature_vec)
    reducer = umap.UMAP(random_state=reducer_seed)
    embedding = reducer.fit_transform(scaled_data)

    # -- plot
    return _2dplot_scatter(embedding, label_vec, title)


def plot_TSNE(feature_vec: np.array, label_vec: np.array, title: Optional[str] = None, reducer_seed: int = 42):
    embedding = TSNE(n_components=2, random_state=reducer_seed).fit_transform(feature_vec)
    return _2dplot_scatter(embedding, label_vec, title)


def _2dplot_scatter(data: np.array, label: np.array, title: Optional[str] = None, marker_size: int = 3):
    fig = plt.figure(figsize=(10, 10))

    max_label = np.max(label)
    palette = seaborn.color_palette()
    if max_label >= len(palette):
        # if not enough colors, use husl palette to always have enough colors
        palette = seaborn.color_palette('husl', max_label + 1)

    plt.scatter(
        data[:, 0],
        data[:, 1],
        s=marker_size,
        c=[palette[int(x)] for x in label]
    )

    plt.gca().set_aspect('equal', 'datalim')
    plt.grid()
    if title is not None:
        plt.title(f'{title}', fontsize=18)

    return fig
