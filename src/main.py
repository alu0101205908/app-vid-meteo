import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output
import dash_vega_components as dvc
from utils.dashboard_utils import *

alt.data_transformers.disable_max_rows()

dash_app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

dash_app.layout = dbc.Container(fluid=True,
    children=[
    dbc.Row([
        dbc.Col(html.H1("Producción vitinicola y avisos fitosanitarios"), className="text-center mb-4")
    ]),

    dbc.Row([
        dbc.Col([
            dvc.Vega(
                id="columnChartTin",
                opt={"renderer": "svg", "actions": False},
                spec=columnChartTin.to_dict(),
                style={'width': '100%', 'height': '100%'}
            ),
        ], width=4),
        dbc.Col([
            dcc.Graph(
                id='mapa',
                figure=mapaChart
            )
        ], width=4),
        dbc.Col([
            dvc.Vega(
                id="columnChartBlan",
                opt={"renderer": "svg", "actions": False},
                spec=columnChartBlan.to_dict(),
                style={'width': '100%', 'height': '100%'}
            )
        ], width=4)
    ]),

    dbc.Row([
        dbc.Col([
            dvc.Vega(
                id="altair-chart",
                opt={"renderer": "svg", "actions": False},
                spec=heatmap.to_dict(),
                style={'width': '100%', 'height': '100%'}
            ),
        ], width=6),
        dbc.Col([
            dvc.Vega(
                id="areaChart",
                opt={"renderer": "svg", "actions": False},
                spec=areaChart.to_dict(),
                style={'width': '100%', 'height': '100%'}
            )
        ], width=6)
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.H4("Total producción", className="card-title"),
                    html.P(id="produccion-total-text", className="card-text"),
                ], style=TEXT_STYLE),
                style=CARD_STYLE
            )
        ], width=6),
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.H4("Total alertas fitosanitarias", className="card-title"),
                    html.P(id="alertas-total-text", className="card-text"),
                ], style=TEXT_STYLE),
                style=CARD_STYLE
            )
        ], width=6)
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.H4("Producción Tinto", className="card-title"),
                    html.P(id="produccion-tinto-text", className="card-text"),
                ], style=TEXT_STYLE),
                style=CARD_STYLE
            )
        ], width=3),
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.H4("Producción Blanco", className="card-title"),
                    html.P(id="produccion-blanco-text", className="card-text"),
                ], style=TEXT_STYLE),
                style=CARD_STYLE
            )
        ], width=3),
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.H4("BOTRYTIS", className="card-title"),
                    html.P(id="alertas-botrytis-text", className="card-text"),
                ], style=TEXT_STYLE),
                style=CARD_STYLE
            )
        ], width=2),
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.H4("MILDIU", className="card-title"),
                    html.P(id="alertas-mildu-text", className="card-text"),
                ], style=TEXT_STYLE),
                style=CARD_STYLE
            )
        ], width=2),
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.H4("OIDIO", className="card-title"),
                    html.P(id="alertas-oidio-text", className="card-text"),
                ], style=TEXT_STYLE),
                style=CARD_STYLE
            )
        ], width=2)
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='periodo-dropdown',
                options=[{'label': str(per), 'value': per} for per in periodos_total],
                value=periodos_total[0],
                clearable=False,
                style={"margin-bottom": "1rem", "width": "100%"}
            )
        ], width=6),
        dbc.Col([
            dcc.Dropdown(
                id='comarca-dropdown',
                options=[{'label': grp, 'value': grp} for grp in df_avisos['comarca_nombre'].unique()],
                value=df_avisos['comarca_nombre'].unique()[0],
                clearable=False,
                style={"margin-bottom": "1rem", "width": "100%"}
            )
        ], width=6),
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='temp-graph')
        ], width=4),
        dbc.Col([
            dcc.Graph(id='hum-graph'),
        ], width=4),
        dbc.Col([
            dcc.Graph(id='rad-graph'),
        ], width=4)
    ])
])

@dash_app.callback(
    [
        Output('produccion-total-text', 'children'),
        Output('alertas-total-text', 'children'),
        Output('produccion-blanco-text', 'children'),
        Output('produccion-tinto-text', 'children'),
        Output('alertas-botrytis-text', 'children'),
        Output('alertas-mildu-text', 'children'),
        Output('alertas-oidio-text', 'children'),
    ],
    [Input('comarca-dropdown', 'value'),
     Input('periodo-dropdown', 'value')]
)
def actualizar_produccion(grupo_seleccionado, periodo_seleccionado):

    dfProd_filtrado = dfProd[(dfProd['comarca_nombre'] == grupo_seleccionado) & (dfProd['year'] == periodo_seleccionado)]
    df_alert_filtrado = df_avisos[(df_avisos['comarca_nombre'] == grupo_seleccionado) & (df_avisos['year'] == periodo_seleccionado)]
    
    produccion_total = dfProd_filtrado['Total'].sum()
    produccion_blanco = dfProd_filtrado['Blanco'].sum()
    produccion_tinto = dfProd_filtrado['Tinto'].sum()
    total_alertas = df_alert_filtrado.size
    df_alertas_a = df_alert_filtrado.loc[df_alert_filtrado["plaga_enfermedad"] == "BOTRYTIS"].size
    df_alertas_b = df_alert_filtrado.loc[df_alert_filtrado["plaga_enfermedad"] == "MILDIU"].size
    df_alertas_c = df_alert_filtrado.loc[df_alert_filtrado["plaga_enfermedad"] == "OIDIO"].size
    
    porcentaje_blanco = (produccion_blanco / produccion_total * 100) if produccion_total else 0
    porcentaje_tinto = (produccion_tinto / produccion_total * 100) if produccion_total else 0
    porcentaje_alertas_a = (df_alertas_a / total_alertas * 100) if total_alertas else 0
    porcentaje_alertas_b = (df_alertas_b / total_alertas * 100) if total_alertas else 0
    porcentaje_alertas_c = (df_alertas_c / total_alertas * 100) if total_alertas else 0
    
    return (
        f"{produccion_total:,} litros",
        f"{total_alertas:,} alertas",
        f"{produccion_blanco:,} litros ({porcentaje_blanco:.1f}%)",
        f"{produccion_tinto:,} litros ({porcentaje_tinto:.1f}%)",
        f"{df_alertas_a:,} alertas ({porcentaje_alertas_a:.1f}%)",
        f"{df_alertas_b:,} alertas ({porcentaje_alertas_b:.1f}%)",
        f"{df_alertas_c:,} alertas ({porcentaje_alertas_c:.1f}%)",
    )


@dash_app.callback(
    [Output('hum-graph', 'figure'),
     Output('rad-graph', 'figure'),
     Output('temp-graph', 'figure')],
    [Input('comarca-dropdown', 'value')])
def update_graphs(selected_comarca):
    temp_fig = meteo_prod('TEMP', selected_comarca)
    hum_fig = meteo_prod('HUM', selected_comarca)
    rad_fig = meteo_prod('RAD', selected_comarca)

    return temp_fig, hum_fig, rad_fig


if __name__ == "__main__":
    dash_app.run_server(debug=True)
