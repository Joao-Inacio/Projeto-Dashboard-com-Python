import json

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output

# Importação da base de dados
df = pd.read_csv("HIST_PAINEL_COVIDBR_2022_Parte1_04nov2022.csv", sep=";")

# Usando só com os estados
df_states = df[(~df["estado"].isna()) & (df["codmun"].isna())]

# Pegando a região do brasil
df_brasil = df[df["regiao"] == "Brasil"]

# Abrindo e lendo o Geo Json
brazil_states = json.load(open("geojson/brazil_geo.json", "r"))

# ponto de partida
df_states_ = df_states[df_states["data"] == "2022-01-01"]

# Criando um app dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

# Criando o mapa
fig = px.choropleth_mapbox(
    df_states_, locations="estado", color="casosNovos", center={"lat": -16.95, "lon": -47.78}, geojson=brazil_states, color_continuous_scale="Redor", opacity=0.4,
    hover_data={"casosAcumulado": True, "casosNovos": True,
                "obitosNovos": True, "estado": True}
)
fig.update_layout(
    mapbox_style="carto-darkmatter"
)

# construindo o layout
app.layout = dbc.Container(
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="choropleth-map", figure=fig)
        ])
    ])
)
if __name__ == "__main__":
    # rodando
    app.run_server(debug=True)
