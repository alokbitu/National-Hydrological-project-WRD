import csv
import io
import math

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import mysql.connector
from threading import Lock
import pandas as pd
from dash.exceptions import PreventUpdate
from app import app

# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

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
    dcc.Location(id='urlars', refresh=True),
    html.H4('Rainfall(ARG)'),
    html.Hr(),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='field-dropdown3',
                options=[
                    {'label': 'ARG', 'value': 'ARG'},
                ],
                placeholder="Station Type"
            ),
        ]),
        dbc.Col([
            dcc.Dropdown(
                id='location-dropdown3',
                options=[],
                placeholder="Location"
            ),
        ]),
        dbc.Col([
            dcc.Dropdown(
                id='station-dropdown3',
                options=[],
                placeholder="Station ID"
            ),
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.Button('Chart View', id='chart-button3', n_clicks=0),
            html.Div(id='output-container3'),
            html.Div(id='graph-container3'),
            dcc.Store(id='data-store3'),
            dcc.Interval(id='interval-component3', interval=60 * 1000, n_intervals=0),
        ]),

        dbc.Col([
            html.Button('Table View', id='table-button3', n_clicks=0),

            html.Button('Report Download', id='report-button3', n_clicks=0),
            dcc.Download(id='download-report3'),
            html.Div(id='table-container3'),
            html.Div(id='report-container3'),
            dcc.Interval(
                id='report_interval-component3',
                interval=60000,  # 1 minute in milliseconds
                n_intervals=0
            )
        ]),
    ], className="mt-2")
])


@app.callback(
    Output('location-dropdown3', 'options'),
    [Input('field-dropdown3', 'value')]
)
def update_location_options(field):
    if field is not None:
        cursor.execute("SELECT DISTINCT stn_location FROM stn_master WHERE stn_type = %s", (field,))
        location_options = [{'label': stn_location, 'value': stn_location} for stn_location, in cursor.fetchall()]
        return location_options
    return []


@app.callback(
    Output('station-dropdown3', 'options'),
    [Input('field-dropdown3', 'value'),
     Input('location-dropdown3', 'value')]
)
def update_station_options(field, stn_location):
    if field is not None and stn_location is not None:
        cursor.execute(
            "SELECT DISTINCT stn_id FROM stn_master WHERE stn_type = %s AND stn_location = %s",
            (field, stn_location)
        )
        station_options = [{'label': stn_id, 'value': stn_id} for stn_id, in cursor.fetchall()]
        return station_options
    return []


@app.callback(
    Output('table-container3', 'children'),
    [Input('station-dropdown3', 'value'),
     Input('field-dropdown3', 'value'),
     Input('table-button3', 'n_clicks'),
     Input('report_interval-component3', 'n_intervals')]
)
def display_table(stn_id, field, table_clicks, n_intervals):
    if table_clicks is not None and table_clicks > 0 and stn_id is not None and field is not None:
        conn2 = mysql.connector.connect(user='root', password='admin123', host='localhost', database='wrd_dash',
                                        auth_plugin='mysql_native_password')
        cur2 = conn2.cursor()
        query2 = "SELECT datetime, hourly_rainfall, daily_rainfall, battery_voltage, solar_voltage FROM arg WHERE stn_id = %s AND stn_type = %s ORDER BY datetime DESC LIMIT 10"
        cur2.execute(query2, (stn_id, field))
        rows = cur2.fetchall()
        # print(rows)
        cur2.close()
        conn2.close()
        list_of_lists = [[str(item) for item in tpl] for tpl in rows]
        if len(rows) == 0:
            return 'No information found for station {} in field {}'.format(stn_id, field)
        else:
            headers = ['DATE & TIME', 'Hr_Rain Fall(mm)','Daily_Rain Fall(mm)', 'Battery Voltage(V)', 'Solar Voltage(V)']
            table = html.Div([
                html.Table(
                    [html.Tr([html.Th(col) for col in headers], style={'background-color': '#D5DBDB', 'padding': '10px'})] +
                    [html.Tr([html.Td(str(cell).replace('T', ' ')) for cell in row], style={'padding': '10px', 'font-size': '12px'}) for row in rows],
                    style={'border-collapse': 'collapse', 'margin-bottom': '20px', 'font-size': '12px'}
                )
            ], id='table-container3')
            return table
    return html.Div()


@app.callback(
    [Output('data-store3', 'data'), Output('graph-container3', 'children')],
    [Input('station-dropdown3', 'value'),
     Input('field-dropdown3', 'value'),
     Input('chart-button3', 'n_clicks'),
     Input('interval-component3', 'n_intervals')],
    [State('data-store3', 'data')]
)
def update_data_store_and_display_graph(stn_id, field, chart_clicks, n_intervals, stored_data):
    if n_intervals > 0:
        global graph_data
        if stn_id is not None and field is not None:
            conn1 = mysql.connector.connect(user='root', password='admin123', host='localhost', database='wrd_dash',
                                            auth_plugin='mysql_native_password')
            cur1 = conn1.cursor()
            cur1.execute(
                "SELECT datetime, hourly_rainfall, daily_rainfall, battery_voltage, solar_voltage FROM arg WHERE stn_id = %s AND stn_type = %s ORDER BY datetime DESC LIMIT 10",
                (stn_id, field)
            )
            fetched_data = cur1.fetchall()
            cur1.close()
            conn1.close()

            with lock:
                graph_data = fetched_data

            if len(fetched_data) == 0:
                return None, ''
            else:
                headers = ['DATE & TIME', 'Hr_Rain Fall(mm)','Daily_Rain Fall(mm)', 'Battery Voltage(V)', 'Solar Voltage(V)']
                data = [headers]
                for row in fetched_data:
                    data.append([str(item) for item in row])
                stored_data = data

        if chart_clicks > 0 and stored_data is not None:
            # Process data and create the graph...

            headers = stored_data[0]
            data_rows = stored_data[1:]

            # Extract x-axis labels and y-axis values for each column
            x_values = []
            y_values = [[] for _ in range(len(headers) - 1)]
            for row in data_rows:
                x_values.append(row[0])
                for i in range(len(row) - 1):
                    y_values[i].append(float(row[i + 1]))

            # Create traces for each column
            traces = []
            for i in range(len(headers) - 1):
                trace = go.Scatter(
                    x=x_values,
                    y=y_values[i],
                    mode='lines + markers',
                    name=headers[i + 1]
                )
                traces.append(trace)

            # Create the layout for the graph
            layout = go.Layout(
                title='Rainfall and Voltage Data',
                xaxis=dict(
                    title='Date & Time',
                    showticklabels=True,
                    tickangle=45,
                    tickformat='%M:%S'
                ),
                yaxis=dict(
                    title='Value'
                ),
                hovermode='x unified'
            )

            # Create the figure and add the traces
            fig = go.Figure(data=traces, layout=layout)

            # Create the graph
            graph = dcc.Graph(
                id='rainfall-graph',
                figure=fig
            )

            return None, graph
    return None, ''

@app.callback(
    [Output('download-report3', 'data'), Output('report-container3', 'children')],
    [Input('station-dropdown3', 'value'),
     Input('field-dropdown3', 'value'),
     Input('report-button3', 'n_clicks')]
     # Input('report_interval-component', 'n_intervals')]
)
def download_report(stn_id, field, report_clicks):
    if report_clicks is not None and report_clicks > 0 and stn_id is not None and field is not None:
        cursor.execute(
            "SELECT datetime, hourly_rainfall, daily_rainfall, battery_voltage, solar_voltage FROM arg WHERE stn_id = %s AND stn_type = %s ORDER BY datetime DESC LIMIT 10",
            (stn_id, field)
        )
        rows = cursor.fetchall()
        headers = ['DATE & TIME', 'Hr_Rain Fall(mm)','Daily_Rain Fall(mm)', 'Battery Voltage(V)', 'Solar Voltage(V)']
        csv_string = io.StringIO()
        writer = csv.writer(csv_string, delimiter=',')
        writer.writerow(headers)
        for row in rows:
            writer.writerow(row)
        csv_string.seek(0)
        return dict(content=csv_string.getvalue(), filename='report.csv'), html.Div('Report downloaded successfully.')
    return None, html.Div()
