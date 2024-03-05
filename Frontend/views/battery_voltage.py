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
# app = dash.Dash(__name__)

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
    dcc.Location(id='urlbatt', refresh=True),
    html.H4('Battery Voltage'),
    html.Hr(),
    dbc.Row([
        dbc.Col([dcc.Dropdown(
            id='field-dropdown2',
            options=[
                {'label': 'AWL', 'value': 'AWL'},
                {'label': 'ARG', 'value': 'ARG'},
                {'label': 'ARG+AWL', 'value': 'ARG+AWL'}
            ],
            placeholder="Station Type"
        ),
        ]),
        dbc.Col([
            dcc.Dropdown(
                id='location-dropdown2',
                options=[],
                placeholder="Location"
            ),
        ]),
        dbc.Col([dcc.Dropdown(
            id='station-dropdown2',
            options=[],
            placeholder="Station ID"
        ),
        ])
    ]),
    dbc.Row([
        dbc.Col([html.Button('Chart View', id='chart-button2', n_clicks=0),
                 html.Div(id='output-container2'),
                 html.Div(id='graph-container2'),
                 dcc.Store(id='data-store2'),
                 dcc.Interval(id='interval-component2', interval=60 * 1000, n_intervals=0),
                 ]),

        dbc.Col([
            html.Button('Table View', id='table-button2', n_clicks=0),
            html.Button('Report Download ', id='report-button2',n_clicks=0),
            dcc.Download(id='download-report2'),
            html.Div(id='table-container2'),
            html.Div(id='report-container2'),
            dcc.Interval(
                id='report_interval-component2',
                interval=60000,  # 1 minute in milliseconds
                n_intervals=0
            ),
        ]),
    ],className="mt-2")
])

@app.callback(
    Output('location-dropdown2', 'options'),
    [Input('field-dropdown2', 'value')]
)
def update_location_options(field):
    if field is not None:
        cursor.execute("SELECT DISTINCT stn_location FROM stn_master WHERE stn_type = %s", (field,))
        location_options = [{'label': stn_location, 'value': stn_location} for stn_location, in cursor.fetchall()]
        return location_options
    return []
@app.callback(
    Output('station-dropdown2', 'options'),
    [Input('field-dropdown2', 'value'),
     Input('location-dropdown2', 'value')]
)
def update_station_options(field, stn_location):
    if field is not None and stn_location is not None:
        cursor.execute("SELECT DISTINCT stn_id FROM stn_master WHERE stn_type = %s AND stn_location = %s", (field, stn_location))
        station_options = [{'label': stn_id, 'value': stn_id} for stn_id, in cursor.fetchall()]
        return station_options
    return []

@app.callback(
Output('table-container2', 'children'),
    [Input('station-dropdown2', 'value'),
     Input('field-dropdown2', 'value'),
     Input('table-button2', 'n_clicks'),
     Input('report_interval-component2', 'n_intervals')]
)
def display_table(stn_id, field, table_clicks, n_interval):
    if table_clicks is not None and table_clicks > 0 and stn_id is not None and field is not None:
        conn7 = mysql.connector.connect(user='root', password='admin', host='localhost', database='wrd_dash',
                                        auth_plugin='mysql_native_password')
        cur7 = conn7.cursor()
        query7 = "SELECT datetime, battery_voltage, solar_voltage FROM realtime_data_query_table WHERE stn_id = %s AND stn_type = %s ORDER BY datetime DESC LIMIT 10"
        cur7.execute(query7, (stn_id, field,))
        rows = cur7.fetchall()
        print(rows)
        cur7.close()
        conn7.close()

        list_of_lists = [[str(item) for item in tpl] for tpl in rows]
        if len(rows) == 0:
            return 'No information found for station {} in field {}'.format(stn_id, field), None
        else:
            headers = ['DATE & TIME', 'Battery Voltage(V)', 'Solar Voltage(V)']
            table = html.Div([
                html.Table(
                    [html.Tr([html.Th(col) for col in headers],
                             style={'background-color': '#D5DBDB', 'padding': '10px'})] +
                    [html.Tr([html.Td(str(cell).replace('T', ' ')) for cell in row],
                             style={'padding': '10px', 'font-size': '12px'}) for row in rows],
                    style={'border-collapse': 'collapse', 'margin-bottom': '20px', 'font-size': '12px'}
                )
            ], id='table-container4')
            return table
    return html.Div()

@app.callback(
    [Output('data-store2', 'data'),
    Output('graph-container2', 'children')],
    [Input('station-dropdown2', 'value'),
     Input('field-dropdown2', 'value'),
     Input('chart-button2', 'n_clicks'),
     Input('interval-component2', 'n_intervals')],
    [State('data-store2', 'data')]
)
def update_data_store_and_display_graph(stn_id, field,chart_clicks, n_intervals, stored_data):
    if n_intervals > 0:
        global graph_data
        if stn_id is not None and field is not None:
            conn8 = mysql.connector.connect(user='root', password='admin', host='localhost', database='wrd_dash',
                                            auth_plugin='mysql_native_password')
            cur8 = conn8.cursor()
            cur8.execute(
                "SELECT datetime, battery_voltage, solar_voltage FROM realtime_data_query_table WHERE stn_id = %s AND stn_type = %s ORDER BY datetime DESC LIMIT 10",
                (stn_id, field)
            )
            fetched_data = cur8.fetchall()
            cur8.close()
            conn8.close()

            with lock:
                graph_data = fetched_data

            if len(fetched_data) == 0:
                return None, ''
            else:
                headers = ['DATE & TIME','Battery Voltage(V)', 'Solar Voltage(V)']
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
    [Output('download-report2', 'data'), Output('report-container2', 'children')],
    [Input('station-dropdown2', 'value'),
     Input('field-dropdown2', 'value'),
     Input('report-button2', 'n_clicks')]
     # Input('report_interval-component', 'n_intervals')]
)
def download_report(stn_id, field, report_clicks):
    if report_clicks is not None and report_clicks > 0 and stn_id is not None and field is not None:
        cursor.execute(
            "SELECT  datetime, battery_voltage, solar_voltage FROM realtime_data_query_table WHERE stn_id = %s AND stn_type = %s ORDER BY datetime DESC LIMIT 10",
            (stn_id, field)
        )
        rows = cursor.fetchall()
        headers = ['DATE & TIME', 'Battery Voltage(V)', 'Solar Voltage(V)']
        csv_string = io.StringIO()
        writer = csv.writer(csv_string, delimiter=',')
        writer.writerow(headers)
        for row in rows:
            writer.writerow(row)
        csv_string.seek(0)
        return dict(content=csv_string.getvalue(), filename='report.csv'), html.Div('Report downloaded successfully.')
    return None, html.Div()
