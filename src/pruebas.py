import dash
import dash_html_components as html
import altair as alt
import pandas as pd
import dash_vega_components as dvc
from utils.pre_procesado import *

# Crear una instancia de la aplicación Dash
app = dash.Dash(__name__)

dfProdAgg = dfProdAgg.loc[~dfProdAgg['comarca_nombre'].isin(["TOTAL"])]
dfProdAgg = dfProdAgg.loc[dfProdAgg["year"].isin(periodos_total)]

columnChartTin = alt.Chart(dfProdAgg).mark_bar().encode(
    x=alt.X('year:O', title='Año'),
    y=alt.Y('sum(Tinto):Q', title='Producción (litros)'),
    color=alt.Color('comarca_nombre:N', title='Comarcas', scale=alt.Scale(domain=comarcas, range=colores)),
    tooltip=['year', 'comarca_nombre', 'sum(Tinto)']
).properties(
    width=600,
    height=500,
    title='Producción total vino tinto'
)

columnChartBlan = alt.Chart(dfProdAgg).mark_bar().encode(
    x=alt.X('year:O', title='Año'),
    y=alt.Y('sum(Blanco):Q', title='Producción (litros)'),
    color=alt.Color('comarca_nombre:N', title='Comarcas', scale=alt.Scale(domain=comarcas, range=colores)),
    tooltip=['year', 'comarca_nombre', 'sum(Blanco)']
).properties(
    width=600,
    height=500,
    title='Producción total vino blanco'
)


chart_dict_tinto = columnChartTin.to_dict()
chart_dict_blanco = columnChartBlan.to_dict()

# Crear una instancia de la aplicación Dash
app = dash.Dash(__name__)

# Layout de la aplicación
app.layout = html.Div([
    html.H1("Visualización de Avisos"),
    html.Div(
        dvc.Vega(
            spec=chart_dict_tinto
        ),
        style={'width': '100%', 'height': '100%'}
    ),
    html.Div(
        dvc.Vega(
            spec=chart_dict_blanco
        ),
        style={'width': '100%', 'height': '100%'}
    )
])

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)