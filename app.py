import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash(__name__)
server = app.server

df = pd.read_csv('nama_10_gdp/nama_10_gdp_1_Data.csv', error_bad_lines = False, engine = 'python', na_values = [':', 'NaN'])

eu_values = [
    'European Union (current composition)',
    'European Union (without United Kingdom)',
    'European Union (15 countries)',
    'Euro area (EA11-2000, EA12-2006, EA13-2007, EA15-2008, EA16-2010, EA17-2013, EA18-2014, EA19)',
    'Euro area (19 countries)',
    'Euro area (12 countries)'
            ]

eu_filter = df['GEO'].isin(eu_values)

df = df.loc[~eu_filter.values].reset_index(drop = True)
df['NA_ITEM_UNIT'] = df['NA_ITEM'] + ' (' + df['UNIT'] + ')'

available_indicators = df['NA_ITEM_UNIT'].unique()
available_countries = df['GEO'].unique()

app.layout = html.Div([
    html.Div([
      html.H1('EUROSTAT DATA Graph 1', style={'text-align': 'center', 'marginBottom': 25,'font-family': 'Arial'}),

        html.Div([
            dcc.Dropdown(
                id = 'xaxis-column',
                options = [{'label': i, 'value': i} for i in available_indicators],
                value = available_indicators[0],
                style = {'font-size': '12px', 'font-family': 'Arial, Helvetica, sans-serif'}
            ),
            dcc.RadioItems(
                id = 'xaxis-type',
                options = [{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value = 'Linear',
                labelStyle = {'display': 'inline-block'},
            )
        ],
        style = {'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id = 'yaxis-column',
                options = [{'label': i, 'value': i} for i in available_indicators],
                value = available_indicators[1],
                style = {'font-size': '10px', 'font-family': 'Arial, Helvetica, sans-serif'}
            ),
            dcc.RadioItems(
                id = 'yaxis-type',
                options = [{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value = 'Linear',
                labelStyle = {'display': 'inline-block'},
            )
        ], style = {'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id = 'indicator-graphic'),
    html.Div([
        dcc.Slider(
            id = 'year--slider',
            min = df['TIME'].min(),
            max = df['TIME'].max(),
            value = df['TIME'].max(),
            step = None,
            marks = {str(year): str(year) for year in df['TIME'].unique()}
        )
    ],
        style = {'margin' : '40px 80px'}
    ),

    html.Div([
      html.H1('EUROSTAT DATA Graph 2', style={'text-align': 'center', 'marginBottom': 25,'font-family': 'Arial'}),

        html.Div([
            dcc.Dropdown(
                id = 'country_2',
                options = [{'label': i, 'value': i} for i in available_countries],
                value = available_countries[0],
                style = {'font-size': '10px', 'font-family': 'Arial, Helvetica, sans-serif'}
            )
        ],
        style = {'width': '48%', 'display': 'inline-block', 'height': '130px'}),

        html.Div([
            dcc.Dropdown(
                id = 'yaxis-column_2',
                options = [{'label': i, 'value': i} for i in available_indicators],
                value = available_indicators[0],
                style = {'font-size': '10px', 'font-family': 'Arial, Helvetica, sans-serif'}
            )
        ],
        style = {'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ],
        style = {'margin-top': '20px'}
    ),

    dcc.Graph(id = 'indicator-graphic_2')
])

@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('xaxis-type', 'value'),
     dash.dependencies.Input('yaxis-type', 'value'),
     dash.dependencies.Input('year--slider', 'value')])

def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    dff = df[df['TIME'] == year_value]

    return {
        'data': [go.Scatter(
            x = dff[dff['NA_ITEM_UNIT'] == xaxis_column_name]['Value'],
            y = dff[dff['NA_ITEM_UNIT'] == yaxis_column_name]['Value'],
            text = dff[dff['NA_ITEM_UNIT'] == yaxis_column_name]['GEO'],
            mode = 'markers',
            marker = {
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis = {
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis = {
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin = {'l': 40, 'b': 40, 't': 40, 'r': 40},
            hovermode = 'closest'
        )
    }

@app.callback(
    dash.dependencies.Output('indicator-graphic_2', 'figure'),
    [dash.dependencies.Input('country_2', 'value'),
     dash.dependencies.Input('yaxis-column_2', 'value')])
def update_graph(country_name, yaxis_column_name):
    return {
        'data': [go.Scatter(
            x = df[(df['GEO'] == country_name) & (df['NA_ITEM_UNIT'] == yaxis_column_name)]['TIME'].values,
            y = df[(df['GEO'] == country_name) & (df['NA_ITEM_UNIT'] == yaxis_column_name)]['Value'].values,
            mode = 'lines'
        )],
        'layout': go.Layout(
            yaxis = {
                'title': yaxis_column_name,
                'type': 'linear'
            },
            margin = {'l': 40, 'b': 40, 't': 40, 'r': 40},
            hovermode = 'closest'
        )
    }

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

if __name__ == '__main__':
    app.run_server()
