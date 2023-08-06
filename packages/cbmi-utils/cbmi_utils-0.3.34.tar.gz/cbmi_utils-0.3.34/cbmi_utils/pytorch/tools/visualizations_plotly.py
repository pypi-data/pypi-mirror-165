from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from jupyter_dash import JupyterDash
from dash import dcc, html, Input, Output, no_update
import base64
import io
from io import BytesIO

from PIL import Image

from typing import Optional

def plot_TSNE_with_images(
    feature_vec: np.array,
    label_vec: np.array,
    imgs: np.array,
    point_class_belonging: list = None,
    title: Optional[str] = None,
    marker_size: float = 3,
    marker_opacity: float = 0.8,
    reducer_seed: int = 42,
    **tsne_args,
):
    """
    This function creates an interactive chart (plotly) by reducing the
    features (with TSNE) of "feature_vec" and creating a scatter plot
    with the results. Each data point is given its own color by a
    label ("label_vec"). When you go over a data point, you can visualize
    an image specified by "imgs". If you have multiple sources, you can use
    the "point_class_belonging" parameter.
    
    params:
        feature_vec:
            A 2D vector, where each data point has his own 1D vector.
        label_vec: 
            A 1D vector , where each data point has a integer as class label.
        imgs:
            A vector where each data point has his own image to show by mouse over.
        point_class_belonging (optional):
            If the source comes from different sources, this parameter helps
            you describe how many data points exists. This parameter is a 2D
            vector, for example [['PyCam', 123],['Kather', 456]]. In this case,
            the first 123 samples comes from the source 'PyCam' and the following
            456 samples belongs to the source 'Kather'.
        title (optional):
            The title of the plot
        reducer_seed (optional):
            The seed that is used for the reducing of the feature space.
        marker_size (optional):
            The size of the marker.
        marker_opacity (optional):
            The opacity of the marker.
        **tsne_args (optional):
            See sklearn.manifold.TSNE for parameters that you can use.
    """
    embedding = TSNE(
        n_components=2,
        random_state=reducer_seed,
        init='pca',
        learning_rate='auto',
        n_jobs=-1,
        **tsne_args,
    ).fit_transform(feature_vec)
    _2dplot_scatter_with_images(
        embedding,
        label_vec,
        imgs,
        point_class_belonging,
        title,
        marker_size,
        marker_opacity,
    )


def plot_PCA_with_images(
    feature_vec: np.array,
    label_vec: np.array,
    imgs: np.array,
    point_class_belonging: list = None,
    title: Optional[str] = None,
    marker_size: float = 3,
    marker_opacity: float = 0.8,
    reducer_seed: int = 42,
):
    """
    This function creates an interactive chart (plotly) by reducing the
    features (with PCA) of "feature_vec" and creating a scatter plot
    with the results. Each data point is given its own color by a
    label ("label_vec"). When you go over a data point, you can visualize
    an image specified by "imgs". If you have multiple sources, you can use
    the "point_class_belonging" parameter.
    
    params:
        feature_vec:
            A 2D vector, where each data point has his own 1D vector.
        label_vec: 
            A 1D vector , where each data point has a integer as class label.
        imgs:
            A vector where each data point has his own image to show by mouse over.
        point_class_belonging (optional):
            If the source comes from different sources, this parameter helps
            you describe how many data points exists. This parameter is a 2D
            vector, for example [['PyCam', 123],['Kather', 456]]. In this case,
            the first 123 samples comes from the source 'PyCam' and the following
            456 samples belongs to the source 'Kather'.
        title (optional):
            The title of the plot
        reducer_seed (optional):
            The seed that is used for the reducing of the feature space.
        marker_size (optional):
            The size of the marker.
        marker_opacity (optional):
            The opacity of the marker.
    """
    embedding = PCA(
        n_components=2,
        random_state=reducer_seed
    ).fit_transform(feature_vec)
    _2dplot_scatter_with_images(
        embedding,
        label_vec,
        imgs,
        point_class_belonging,
        title,
        marker_size,
        marker_opacity
    )


def _2dplot_scatter_with_images(data: np.array, labels: np.array, imgs: np.array, point_class_belonging: list = None, title: Optional[str] = None, marker_size: float = 3, marker_opacity: float = 0.8):
    if not point_class_belonging:
        point_class_belonging = [['Dataset', len(labels)]]
    num_of_ds = len(point_class_belonging)
    colorscales = [px.colors.sequential.Turbo[i*15//num_of_ds:(i+1)*15//num_of_ds] for i in range(num_of_ds)]
    
    [px.colors.sequential.Turbo[:5], px.colors.sequential.Turbo[5:]] # 'viridis'
    figure_data = []
    pos = 0
    for i, (class_name, num_of_samples) in enumerate(point_class_belonging):
        figure_data.append(
            go.Scatter(
                x=data[pos:pos+num_of_samples, 0],
                y=data[pos:pos+num_of_samples, 1],
                mode="markers",
                marker=dict(
                    colorscale=colorscales[i],
                    color=labels[pos:pos+num_of_samples],
                    colorbar={
                        "title": class_name,
                        "x":1.+0.13*i,
                        "titleside":'right',
                        "dtick":1
                    },
                    line={"color": "#000"},
                    reversescale=True,
                    size=marker_size,
                    sizeref=marker_size,
                    sizemode="diameter",
                    opacity=marker_opacity,
                ),
                name=class_name,
            )
        )
        pos = pos+num_of_samples
    
    fig = go.Figure(data=figure_data)
    if title:
        fig.update_layout(title_text=title, title_x=0.5)
    # turn off native plotly.js hover effects - make sure to use
    # hoverinfo="none" rather than "skip" which also halts events.
    fig.update_traces(hoverinfo="none", hovertemplate=None)
    fig.update_layout(
        xaxis=dict(title='Dimension 1'),
        yaxis=dict(title='Dimension 2'),
        plot_bgcolor='rgba(255,255,255,0.1)'
    )
    fig.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ))

    app = JupyterDash(__name__)

    app.layout = html.Div([
        dcc.Graph(id="graph", figure=fig, clear_on_unhover=True),
        dcc.Tooltip(id="graph-tooltip"),
    ])
    @app.callback(
        Output("graph-tooltip", "show"),
        Output("graph-tooltip", "bbox"),
        Output("graph-tooltip", "children"),
        Input("graph", "hoverData"),
    )
    def display_hover(hoverData):
        if hoverData is None:
            return False, no_update, no_update
        # demo only shows the first point, but other points may also be available
        pt = hoverData["points"][0]
        dataset_pos = pt['curveNumber']
        dataset_name = point_class_belonging[dataset_pos][0]
        bbox = pt["bbox"]
        num = int(pt["pointNumber"] + np.sum([c for i, (n,c) in enumerate(point_class_belonging) if i < dataset_pos]))
        
        img = imgs[num]
        buffered = BytesIO()
        Image.fromarray(img).save(buffered, format="PNG")
        img = base64.b64encode(buffered.getvalue()).decode()

        children = [
            html.Div(children=[
                html.Img(src='data:image/png;base64,{}'.format(img), style={"width": "100%"}),
                #html.P(f"Class: {labelname[labels[num]]}", style={"color": "darkblue"}),
                #html.P(f"Filename: {img_src.split('/')[-1]}"),
                html.P(f"Dataset: {dataset_name}", style={"color": "darkblue"}),
                html.P(f"Class: {labels[num]}", style={"color": "darkblue"}),
                html.P(f"Id: {num}", style={"color": "darkblue"}),
            ],
            style={'width': '200px', 'white-space': 'normal'})
        ]

        return True, bbox, children
    app.run_server(debug=True, mode='inline')
