from matplotlib.pyplot import margins
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import numpy as np
import pandas as pd

import os
this_dir, this_filename = os.path.split(__file__)

def selector(name, args):
    return graph_func_lookup[name](*args)

def energy_sources_comp(df: pd.DataFrame):
    df.sort_values(inplace=True)
    df = df.round(2)
    fig = px.bar(
        df,
        orientation='h',
        text_auto=True
    )

    fig.update_layout(
        title_text="Energy Consumption by Type",
        template="simple_white",
        font=dict(size=18),
        margin=dict(l=20, r=20)
    )

    fig.update_xaxes(title_text="Consumption <b>MWh</b>")
    fig.update_yaxes(title_text="Type")
    fig.update_layout(showlegend=False)

    write_path = os.path.join(this_dir, "library", "templates", "content", "energy_sources.svg")
    fig.write_image(write_path)

    return write_path

def ranking_bar_chart(x, y, metric_name):
    y = np.array([10, 12, 15, 19, 28])
    color = np.array(["rgb(255,255,255)"] * y.shape[0])
    color[y < 20] = "rgb(204,204, 205)"
    color[y >= 20] = "rgb(130, 0, 0)"

    fig = go.Figure(
        go.Bar(
            x=x,
            y=y,
            orientation="h",
        )
    )
    fig.update_xaxes(title_text="Data Center (Self Reported)")
    fig.update_yaxes(title_text="Power Usage Effectiveness")

    write_path = os.path.join(this_dir, "library", "templates", "content", "metric_compare.svg")
    fig.write_image(write_path)


def rn_energy_adapt(dc_cons, ren_prod, date):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(y=dc_cons, x=date, name="DC Total Energy"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(y=ren_prod, x=date, name="Grid Renewable Energy"),
        secondary_y=True,
    )

    fig.update_layout(
        title_text="Clean Energy Adaptability",
        template="simple_white",
        font=dict(size=26),
        legend=dict(x=0.55, y=1.2),
        width=950,
        height=700,
    )

    fig.update_xaxes(title_text="Date")

    fig.update_yaxes(title_text="Consumption <b>kWh</b>", secondary_y=False)
    fig.update_yaxes(title_text="Production <b>MWh</b>", secondary_y=True)

    write_path = os.path.join(this_dir, "library", "templates", "content", "rn_energy_adapt.svg")
    fig.write_image(write_path)
    return write_path


graph_func_lookup = {
    "energy_sources_comp": energy_sources_comp,
    "rn_energy_adapt": rn_energy_adapt,
    "ranking_bar_chart": ranking_bar_chart,
}


if __name__ == "__main__":
    # y = ["Google Avg", "this", "DC3 PARIS - Scaleway", "Equinix", "World Average"]
    # x = [1.10, 1.28, 1.35, 1.4, 1.59]
    # ranking_bar_chart(x, y, "Power Usage Effectiviness (PUE)")
    pass