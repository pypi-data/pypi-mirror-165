from __future__ import annotations

import itertools
from typing import Callable, Dict, Optional, Sequence, Tuple, TYPE_CHECKING

from IPython.display import clear_output
from IPython.display import display
import numpy as np
import pandas as pd
import plotly.graph_objects as go

import truera.client.intelligence.visualizations.colors as Colors
from truera.client.intelligence.visualizations.plots import Plots
from truera.rnn.general.aiq.clustering import FEATURE_IDX_KEY
from truera.rnn.general.aiq.clustering import FEATURE_KEY
from truera.rnn.general.aiq.clustering import PARENT_ID_KEY
from truera.rnn.general.aiq.clustering import X_KEY
from truera.rnn.general.aiq.clustering import Y_KEY

if TYPE_CHECKING:
    from truera.nlp.general.aiq.aiq import SentenceInfo


class InteractionPlots(Plots):
    """
    A Visualization Class for interaction workflows.
    """

    @staticmethod
    def gradient_landscape_graph(
        record_info: Tuple[pd.DataFrame, Sequence[str]],
        record_idx: Sequence[int],
        figsize: Optional[Tuple[int, int]] = (800, 400)
    ) -> go.Figure:
        """
        Visualize the gradient paths by feature.

        Args:
            record_info (tuple[pd.DataFrame, list[str]]): Supplementary information about the record. 
                The dataframe will contain gradient path info. The list[str] are the corresponding feature names
            record_idx (int): The record to show gradient paths for.
            figsize: Size for plot in pixels. Defaults to (800, 400).
        Returns:
            go.Figure: the visualization
        """
        landscape_df, _ = record_info[record_idx]

        layout = go.Layout(
            plot_bgcolor=Colors.WHITE,
            hoverlabel=dict(
                bgcolor=Colors.TRUERA_GREEN,
                font_size=16,
            ),
            width=figsize[0],
            height=figsize[1],
            uniformtext_minsize=20,
            xaxis=dict(title="Step Number"),
            yaxis=dict(title="Gradient Magnitude"),
            title={
                "text": "Gradient Landscape from Baseline",
                "x": 0.5,
                "xanchor": "center"
            }
        )
        fig = go.Figure(layout=layout)

        for feature_name in landscape_df.columns:
            landscape_scatter = go.Scatter(
                y=landscape_df[feature_name], mode="lines", name=feature_name
            )
            fig.add_trace(landscape_scatter)
        return fig

    @staticmethod
    def feature_interaction_dendrogram(
        record_info: Tuple[pd.DataFrame, Sequence[str]],
        record_idx: Sequence[int],
        figsize: Optional[Tuple[int, int]] = (800, 800)
    ) -> go.Figure:
        """
        Visualize the feature interaction via dendrogram of similar features

        Args:
            record_info (tuple[pd.DataFrame, list[str]]): Supplementary information about the record. 
                The dataframe will contain gradient path info. The list[str] are the corresponding feature names
            record_idx (int): The record to show gradient paths for.
            figsize: Size for plot in pixels. Defaults to (800, 800).
        Returns:
            go.Figure: the visualization
        """
        landscape_df, _ = record_info[record_idx]
        f_df = landscape_df[landscape_df[FEATURE_KEY].notnull()]
        has_parent_df = landscape_df[landscape_df[PARENT_ID_KEY].notnull()]

        hide_axis = dict(
            showline=False,
            zeroline=False,
            showgrid=False,
            showticklabels=False,
        )
        layout = go.Layout(
            plot_bgcolor=Colors.WHITE,
            hoverlabel=dict(
                bgcolor=Colors.TRUERA_GREEN,
                font_size=16,
            ),
            showlegend=False,
            width=figsize[0],
            height=figsize[1],
            uniformtext_minsize=20,
            xaxis=hide_axis,
            yaxis=hide_axis,
            title={
                "text": f"Interaction Dendrogram",
                "x": 0.5,
                "xanchor": "center"
            }
        )
        fig = go.FigureWidget(layout=layout)

        edge_xs = has_parent_df.apply(
            lambda row: [landscape_df.loc[int(row.parent_id)].x, row.x, None],
            axis=1
        )
        edge_ys = has_parent_df.apply(
            lambda row: [landscape_df.loc[int(row.parent_id)].y, row.y, None],
            axis=1
        )
        edge_scatter = go.Scatter(
            x=list(itertools.chain.from_iterable(edge_xs)),
            y=list(itertools.chain.from_iterable(edge_ys)),
            mode="lines",
            line=dict(color="rgba(0, 0, 0)", width=1),
            hoverinfo="none",
            opacity=0.8
        )
        fig.add_trace(edge_scatter)

        highlight_edge_scatter = go.Scatter(
            x=[],
            y=[],
            mode="lines",
            line=dict(color="rgba(0, 0, 0)", width=2),
            hoverinfo="none"
        )
        fig.add_trace(highlight_edge_scatter)

        highlight_point_scatter = go.Scatter(
            x=[],
            y=[],
            mode="markers",
            marker=dict(size=10, color="red", line=dict(width=0)),
            hoverinfo="none"
        )
        fig.add_trace(highlight_point_scatter)

        text_scatter = go.Scatter(
            mode="text",
            textposition="middle center",
            x=f_df[X_KEY],
            y=f_df[Y_KEY],
            text=f_df[FEATURE_KEY]
        )
        fig.add_trace(text_scatter)

        click_scatter = go.Scatter(
            x=landscape_df[X_KEY],
            y=landscape_df[Y_KEY],
            mode="markers",
            opacity=0.0
        )
        fig.add_trace(click_scatter)

        root_scatter = go.Scatter(
            x=[landscape_df.loc[0]["x"]],
            y=[landscape_df.loc[0]["y"]],
            mode="markers",
            marker=dict(symbol="star", size=30, line=dict(width=0)),
            opacity=0.8
        )
        fig.add_trace(root_scatter)
        return fig

    @staticmethod
    def token_interaction_bar(
        sentence_info: SentenceInfo,
        corrs: Dict[int, np.ndarray],
        corr_idx_maps: Dict[int, int],
        sentence_idx: int,
        init_word_idx: int = 0,
        min_yaxis: float = 0.0,
        reset_display_func: Callable = None
    ) -> go.Figure:
        """
        Creates a correlation bar graph from a selected token to the other tokens.
        
        Args:
            sentence_info: contains a DataFrame of the spectral clustered tree and the sentence itself
            corrs: the correlation matrix of grad paths. 
            corr_idx_maps: mappings from the correlation matrix ids to the token ids. 
            sentence_idx: the sentence being operated on
            init_word_idx: the ith word in a filtered down token list (for performance reasons)
            reset_display_func: A function that reconstructs display elements. 
                This is needed because of a bug that resizes the display on click; so instead we reset and redisplay
        Returns:
            go.Figure: the visualization
        """
        sentence_df, _ = sentence_info[sentence_idx]
        correlation_matrix = corrs[sentence_idx]
        correlation_idx_map = corr_idx_maps[sentence_idx]
        token_df = sentence_df[sentence_df[FEATURE_IDX_KEY].notnull(
        )].set_index(FEATURE_IDX_KEY).sort_values(by=[FEATURE_IDX_KEY])
        tokens = token_df[FEATURE_KEY].tolist()
        bolded_tokens = tokens[:]
        bolded_tokens[init_word_idx] = f"<b>{tokens[init_word_idx]}</b>"
        num_tokens = len(tokens)

        common_ancestors = np.array(
            [
                [
                    len(
                        set(token_df.iloc[idx1].ancestor_ids
                           ).intersection(token_df.iloc[idx2].ancestor_ids)
                    ) for idx1 in range(num_tokens)
                ] for idx2 in range(num_tokens)
            ]
        )
        layout = Plots.truera_layout(
            xaxis=dict(
                title="Tokens",
                tickmode="array",
                tickvals=np.arange(num_tokens),
                ticktext=bolded_tokens,
                tickangle=-45,
                tickfont=dict(size=18 - int(num_tokens / 10))
            ),
            yaxis=dict(
                title=f"Correlation with \"{tokens[init_word_idx]}\"",
                range=[min_yaxis, 1.0]
            ),
            barmode="stack",
            showlegend=False,
        )

        fig = go.FigureWidget(layout=layout)

        # Reconfigure the correlation matrix to be ordered lowest token id to highest token id
        reverse_corr_idx_map = {
            correlation_idx_map[i]: i for i in range(len(correlation_idx_map))
        }
        sorted_token_ids = [k for k in reverse_corr_idx_map]
        sorted_token_ids.sort()
        token_sorted_correlation_matrix_ids = [
            reverse_corr_idx_map[k] for k in reverse_corr_idx_map
        ]
        correlation_matrix = correlation_matrix[
            token_sorted_correlation_matrix_ids, :]
        correlation_matrix = correlation_matrix[:,
                                                token_sorted_correlation_matrix_ids
                                               ]

        fig.add_trace(
            go.Bar(
                x=np.arange(num_tokens),
                y=correlation_matrix[init_word_idx],
                marker=dict(
                    color=common_ancestors[init_word_idx],
                    colorbar=dict(title="Common Ancestors", dtick=1),
                    colorscale="Blues"
                )
            )
        )
        fig.add_trace(
            go.Bar(
                x=np.arange(num_tokens),
                y=1 - correlation_matrix[init_word_idx],
                opacity=0
            )
        )

        def update_point(trace, points, selector, fig=fig, tokens=tokens):
            if (len(points.point_inds) > 0):
                clear_output(wait=True)
                if reset_display_func is not None:
                    reset_display_func()
                new_idx = points.point_inds[0]
                fig.data[0].y = correlation_matrix[new_idx]
                fig.data[1].y = 1 - correlation_matrix[new_idx]
                fig.data[0].marker.color = common_ancestors[new_idx]

                bolded_tokens = tokens[:]
                bolded_tokens[new_idx] = f"<b>{tokens[new_idx]}</b>"
                fig.layout.xaxis.ticktext = bolded_tokens
                fig.layout.yaxis.title = f"Correlation with \"{tokens[new_idx]}\""
                display(fig)

        fig.data[0].on_click(update_point)
        fig.data[1].on_click(update_point)
        display(fig)
