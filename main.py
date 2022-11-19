import json

import dash
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html
from dash.dependencies import Input, Output

# Importação da base de dados
df = pd.read_csv("HIST_PAINEL_COVIDBR_2022_Parte1_04nov2022.csv", sep=";")

# Usando só com os estados
df_states = df[(~df["estado"].isna()) & (df["codmun"].isna())]

# Pegando a região do brasil
df_brasil = df[df["regiao"] == "Brasil"]

# Abrindo e lendo o Geo Json
brazil_states = json.load(open("geojson/brazil_geo.json", "r"))

# Gráfico de barras
df_data = df_states[df_states["estado"] == "CE"]

# ponto de partida
df_states_ = df_states[df_states["data"] == "2022-01-01"]

select_columns = {
    "casosAcumulado": "Casos Acumulados",
    "casosNovos": "Novos Casos",
    "obitosAcumulado": "Óbitos Totais",
    "obitosNovos": " Óbitos por dia"
}

# Criando um app dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

# Criando o mapa
fig = px.choropleth_mapbox(
    df_states_, locations="estado", color="casosNovos",
    center={"lat": -16.95, "lon": -47.78}, zoom=3, geojson=brazil_states,
    color_continuous_scale="Redor", opacity=0.4,
    hover_data={
        "casosAcumulado": True, "casosNovos": True,
        "obitosNovos": True, "estado": True
    }
)
fig.update_layout(
    paper_bgcolor="#242424",
    autosize=True,
    margin=go.Margin(l=0, r=0, t=0, b=0),
    showlegend=False,
    mapbox_style="carto-darkmatter"
)

# Gráficos de barras
fig2 = go.Figure(layout={"template": "plotly_dark"})
fig2.add_trace(go.Scatter(x=df_data["data"], y=df_data["casosAcumulado"]))
fig2.update_layout(
    paper_bgcolor="#242424",
    plot_bgcolor="#242424",
    autosize=True,
    margin=dict(l=10, r=10, t=10, b=10)
)

# construindo o layout
app.layout = dbc.Container(
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Img(
                    id="logo",
                    src=app.get_asset_url(
                        "logo.png"
                    ),
                    height=50
                ),
                html.H5("Evolução COVID-19"),
                dbc.Button(
                    "BRASIL", color="primary",
                    id="location-button", size="lg"
                )
            ], style={}),
            html.P(
                "Informe  a data na qual deseja obter informações:",
                style={"margin-top": "40px"}
            ),
            html.Div(id="div-teste", children=[
                dcc.DatePickerSingle(
                    id="date-picker",
                    min_date_allowed=df_brasil["data"].min(),
                    max_date_allowed=df_brasil["data"].max(),
                    initial_visible_month=df_brasil["data"].min(),
                    date=df_brasil["data"].max(),
                    display_format="MMMM D, YYYY",
                    style={"border": "0px solid black"}
                )
            ]),

            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Span("Casos Recuperados"),
                            html.H3(
                                style={"color": "#00FFFF"},
                                id="casos-recuperados-text"
                            ),
                            html.Span("Em acompanhamento"),
                            html.H5(id="em-acompanhamento-text"),
                        ])
                    ],  color="light", outline=True,
                        style={
                        "margin-top": "10px",
                        "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                        "color": "#FFFFFF"
                    }),
                ], md=4),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Span("Casos Confirmados Totasi"),
                            html.H3(
                                style={"color": "#389FD6"},
                                id="casos-confirmados-text"
                            ),
                            html.Span("Novos casos na data"),
                            html.H5(id="novos-casos-text"),
                        ])
                    ],  color="light", outline=True,
                        style={
                        "margin-top": "10px",
                        "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                        "color": "#FFFFFF"
                    }),
                ], md=4),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Span("Óbitos Confirmados"),
                            html.H3(
                                style={"color": "#DF2935"},
                                id="obitos-text"
                            ),
                            html.Span("Óbitos na data"),
                            html.H5(id="obitos-na-data-text"),
                        ])
                    ],  color="light", outline=True,
                        style={
                        "margin-top": "10px",
                        "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                        "color": "#FFFFFF"
                    }),
                ], md=4),
            ]),
            html.Div([
                html.P(
                    "Selecione que tipo de dados deseja visualizar:",
                    style={"margin-top": "25px"}
                ),
                dcc.Dropdown(
                    id="location-dropdown",
                    options=[
                        {"label": j, "value": i} for i, j in select_columns.items()],
                    value="casosNovos",
                    style={"margin-top": "10px"}
                ),
                dcc.Graph(id="line-graph", figure=fig2)
            ]),
        ]),
        dbc.Col([
            dcc.Graph(id="choropleth-map", figure=fig)
        ])
    ])
)

if __name__ == "__main__":
    # rodando
    app.run_server(debug=True)
