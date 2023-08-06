import pandas as pd
import plotly.express as px


def plotly_results(
    strand_data: pd.DataFrame,
    column: str,
    figsize=(750, 600),
    xlim=(0, 80),
    ylim=(0, 80),
) -> None:
    """Static method plotting results with plotly package

    :param strand_data: a dataframe with strand positions and field values
    :param xlim: limits in x-direction
    :param ylim: limits in y-direction
    """
    roxie = [
        "rgb(17,0,181)",
        "rgb(11,42,238)",
        "rgb(0,104,236)",
        "rgb(0,154,235)",
        "rgb(0,208,226)",
        "rgb(0,246,244)",
        "rgb(0,255,0)",
        "rgb(116,255,0)",
        "rgb(191,255,0)",
        "rgb(252,255,0)",
        "rgb(255,199,0)",
        "rgb(255,146,0)",
        "rgb(255,86,0)",
        "rgb(255,0,0)",
        "rgb(246,0,0)",
        "rgb(232, 0, 0)",
        "rgb(197, 0, 50)",
        "rgb(168, 0, 159)",
    ]

    fig = px.scatter(
        strand_data,
        x="x, [mm]",
        y="y, [mm]",
        color=column,
        hover_data=[column],
        color_continuous_scale=roxie,
    )
    fig.update_layout(
        autosize=False,
        width=figsize[0],
        height=figsize[1],
        xaxis_range=xlim,
        yaxis_range=ylim,
        plot_bgcolor="rgba(0,0,0,0)",
        images=[
            dict(
                source="https://i.ibb.co/kcc2mbw/ROXIE.png",
                xref="paper",
                yref="paper",
                x=1.16,
                y=-0.05,
                sizex=0.2,
                sizey=0.2,
                xanchor="right",
                yanchor="bottom",
            )
        ],
    )
    fig.show()
