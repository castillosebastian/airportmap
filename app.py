import plotly.graph_objects as go # or plotly.express as px
import dash
from dash import dcc, html
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.io as pio
import polars as pl
import pandas as pd

pio.templates.default = "plotly_dark"

# data
codepl=pl.read_csv('airport_code.csv')
frepl=pl.read_csv('airport_frequencies.csv')
result = codepl.join(frepl, on='ident')
result_us = result.filter(pl.col('iso_country') == 'US')

airports = result.to_pandas()


# define the category levels and their numerical values
category_levels = {
    "small_airport": 0.2,
    "heliport": 0.1,
    "closed": 0,
    "medium_airport": 0.3,
    "seaplane_base": 0.1,
    "large_airport": 0.4,
    "balloonport": 0.1
}

# create an ordered categorical variable based on the string variable
airports["airport_type_ordered"] = pd.Categorical(airports["type"], 
                                            categories=category_levels.keys(),
                                            ordered=True).map(category_levels)

# map
fig = px.scatter_mapbox(airports, lat="latitude_deg", lon="longitude_deg", hover_name="municipality", 
                        hover_data=["municipality", "name", "type"],
                        color="type",
                        zoom=3, height=900,
                        #size="airport_type_ordered",
                        )

fig.update_layout(mapbox_style="open-street-map")

fig.update_layout(margin={"r":50,"t":50,"l":60,"b":50},
                  legend=dict(
                    orientation="h",
                    entrywidth=160,
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1,
                    font=dict(
                        family="Courier",
                        size=20,
                        color="white"
                    ),
                    )
                )
fig.update_layout(legend_title_text='')

fig = go.Figure(fig) # or any Plotly Express function e.g. px.bar(...)

app = dash.Dash(
    __name__, external_stylesheets=[dbc.themes.DARKLY],
)

server = app.server
    
app.layout = html.Div([
    html.Div(
            [
                html.Div(
                    [                        
                        dcc.Markdown(
                            """
                            #   Aeropuertos en el mundo (UTN-VIS)
                            """.replace(
                                            "  ", ""
                                        ),
                            className="title",
                        style={
                            'margin-top': '20px',
                            'margin-left' : '15px',
                            'width' : '100%',                            
                            'lineHeight' : '60px',  
                            }
                        ),                        
                    ]
                ),
                html.Br(),
                dbc.Row(
                    [
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H3(
                                        "Maestría Minería de Datos UTN-Parana: Catedra 'Visualización' 2023",
                                        className="card-title",
                                    ),
                                    html.H5(
                                        [
                                            "Gráfico que contiene los aeropuertos en el mundo. ",                                            
                                        ],
                                        className="card-text",
                                    ),
                                    dbc.CardLink("CSCastillo Github", href="https://github.com/castillosebastian/demo8.git"),
                                ]
                            ),                            
                            style={                            
                            'width' : '100%',  
                            },                             
                    ),
                    ]
                ),                
            ]
        ),
    dcc.Graph(figure=fig,
              config = {'displayModeBar': False,
                        'displaylogo': False}),
    ])

if __name__ == '__main__':
    app.run_server(debug=True)  # Turn off reloader if inside Jupyter