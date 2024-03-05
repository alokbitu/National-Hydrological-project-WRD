import dash
from dash import dcc
from dash import html
import mysql.connector
import pandas as pd
import plotly.express as px
import io
import csv
from app import app
import dash_bootstrap_components as dbc
from threading import Lock
from dash.dependencies import Input, Output, State
import math
import plotly.graph_objects as go

# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN, dbc.icons.BOOTSTRAP], suppress_callback_exceptions=True)
# server = app.server
# Connect to the database
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='admin',
    database='wrd_dash'
)
cursor = connection.cursor()

lock = Lock()
graph_data = []

layout = html.Div([
dcc.Location(id='urlcomb', refresh=True),
    html.H4('Combine-station(ARG+AWL)'),
    html.Hr(),
    dbc.Row([
        dbc.Col([dcc.Dropdown(
            id='field-dropdown5',
            options=[
                {'label': 'ARG+AWL', 'value': 'ARG+AWL'}
            ],
            placeholder="Station Type"
        ),
        ]),
        dbc.Col([
            dcc.Dropdown(
                id='location-dropdown5',
                options=[],
                placeholder="Location"
            ),
        ]),
        dbc.Col([dcc.Dropdown(
            id='station-dropdown5',
            options=[],
            placeholder="Station ID"
        ),
        ])
    ]),
    dbc.Row([
        dbc.Col([html.Button('Chart View', id='chart-button5', n_clicks=0),
                 html.Div(id='output-container5'),
                 html.Div(id='graph-container5'),
                 dcc.Store(id='data-store5'),
                 dcc.Interval(id='interval-component5', interval=60 * 1000, n_intervals=0),
                 ]),

        dbc.Col([html.Button('Table View', id='table-button5', n_clicks=0),
                 html.Button('Report Download', id='report-button5', n_clicks=0),
                 dcc.Download(id='download-report5'),
                 html.Div(id='table-container5'),
                 html.Div(id='report-container5'),
                 dcc.Interval(
                     id='report_interval-component5',
                     interval=60000,  # 1 minute in milliseconds
                     n_intervals=0
                 )
                 ]),
    ],className="mt-2")
])
@app.callback(
    Output('location-dropdown5', 'options'),
    [Input('field-dropdown5', 'value')]
)
def update_location_options(field):
    if field is not None:
        cursor.execute("SELECT DISTINCT stn_location FROM stn_master WHERE stn_type = %s", (field,))
        location_options = [{'label': stn_location, 'value': stn_location} for stn_location, in cursor.fetchall()]
        return location_options
    return []

@app.callback(
    Output('station-dropdown5', 'options'),
    [Input('field-dropdown5', 'value'),
     Input('location-dropdown5', 'value')]
)
def update_station_options(field, stn_location):
    if field is not None and stn_location is not None:
        cursor.execute("SELECT DISTINCT stn_id FROM stn_master WHERE stn_type = %s AND stn_location = %s", (field, stn_location))
        station_options = [{'label': stn_id, 'value': stn_id} for stn_id, in cursor.fetchall()]
        return station_options
    return []

@app.callback(
    Output('table-container5', 'children'),
    [Input('station-dropdown5', 'value'),
    Input('field-dropdown5', 'value'),
     Input('table-button5', 'n_clicks'),
     Input('report_interval-component5', 'n_intervals')]
)
def display_table(stn_id, field, table_clicks, n_intervals):
    if table_clicks is not None and table_clicks > 0 and stn_id is not None and field is not None:
        conn5 = mysql.connector.connect(user='root', password='admin', host='localhost', database='wrd_dash',
                                        auth_plugin='mysql_native_password')
        cur5 = conn5.cursor()
        query3 = "SELECT datetime, hourly_rainfall_value, daily_rainfall_value, water_level_value, battery_voltage, solar_voltage FROM combine_station WHERE stn_id = %s AND stn_type = %s ORDER BY datetime DESC LIMIT 10"
        cur5.execute(query3, (stn_id, field))
        rows = cur5.fetchall()
        print(rows)
        cur5.close()
        conn5.close()
        list_of_lists = [[str(item) for item in tpl] for tpl in rows]
        if len(rows) == 0:
            return 'No information found for station {} in field {}'.format(stn_id, field), None
        else:
            headers = ['DATE & TIME', 'Hr_Rain Fall(mm)','Daily_Rain Fall(mm)','Water Level(m)', 'Battery Voltage(V)', 'Solar Voltage(V)']
            table = html.Div([
                html.Table(
                    [html.Tr([html.Th(col) for col in headers],
                             style={'background-color': '#D5DBDB', 'padding': '10px'})] +
                    [html.Tr([html.Td(str(cell).replace('T', ' ')) for cell in row],
                             style={'padding': '10px', 'font-size': '12px'}) for row in rows],
                    style={'border-collapse': 'collapse', 'margin-bottom': '20px', 'font-size': '12px'}
                )
            ], id='table-container5')
            return table
    return html.Div()


@app.callback(
   [Output('data-store5', 'data'), Output('graph-container5', 'children')],
    [Input('station-dropdown5', 'value'),
     Input('field-dropdown5', 'value'),
Input('chart-button5', 'n_clicks'),
     Input('interval-component5', 'n_intervals')],
    [State('data-store5', 'data')]
)
def update_data_store_and_display_graph(stn_id, field, chart_clicks, n_intervals, stored_data):
    if n_intervals > 0:
        global graph_data
        if stn_id is not None and field is not None:
            conn6 = mysql.connector.connect(user='root', password='admin', host='localhost', database='wrd_dash',
                                            auth_plugin='mysql_native_password')
            cur6 = conn6.cursor()
            cur6.execute(
                "SELECT datetime, hourly_rainfall_value, daily_rainfall_value, water_level_value, battery_voltage, solar_voltage FROM combine_station WHERE stn_id = %s AND stn_type = %s", (stn_id, field,)
            )
            fetched_data = cur6.fetchall()
            cur6.close()
            conn6.close()

            with lock:
                graph_data = fetched_data

            if len(fetched_data) == 0:
                return None, ''
            else:
                headers = ['DATE & TIME', 'Hr_Rain Fall(mm)','Daily_Rain Fall(mm)','water level(m)', 'Battery Voltage(V)', 'Solar Voltage(V)']
                data = [headers]
                for row in fetched_data:
                    data.append([str(item) for item in row])
                stored_data = data

        if chart_clicks > 0 and stored_data is not None:
            headers = stored_data[0]
            df = pd.DataFrame(stored_data[1:], columns=headers, index=[row[0] for row in stored_data[1:]])
            fig = px.line(df, x='DATE & TIME', y=df.columns[1:], title='Station Data', markers=True)
            graph = dcc.Graph(id='station-graph', figure=fig)
            return stored_data, graph

    return None, ''

@app.callback(
    [Output('download-report5', 'data'), Output('report-container5', 'children')],
    [Input('station-dropdown5', 'value'),
     Input('field-dropdown5', 'value'),
     Input('report-button5', 'n_clicks')]
     # Input('report_interval-component', 'n_intervals')]
)
def download_report(stn_id, field, report_clicks):
    if report_clicks is not None and report_clicks > 0 and stn_id is not None and field is not None:
        cursor.execute(
            "SELECT datetime, hourly_rainfall_value, daily_rainfall_value, water_level_value, battery_voltage, solar_voltage FROM ccombine_station WHERE stn_id = %s AND stn_type = %s ORDER BY datetime DESC LIMIT 10",
            (stn_id, field)
        )
        rows = cursor.fetchall()
        headers = ['DATE & TIME', 'Hr_Rain Fall(mm)','Daily_Rain Fall(mm)','water Level(m)', 'Battery Voltage(V)', 'Solar Voltage(V)']
        csv_string = io.StringIO()
        writer = csv.writer(csv_string, delimiter=',')
        writer.writerow(headers)
        for row in rows:
            writer.writerow(row)
        csv_string.seek(0)
        return dict(content=csv_string.getvalue(), filename='report.csv'), html.Div('Report downloaded successfully.')
    return None, html.Div()

# if __name__ == '__main__':
#     app.run_server(debug=True)
