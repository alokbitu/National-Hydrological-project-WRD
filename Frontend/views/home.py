import base64
import csv
import io
import dash_core_components as dcc
import dash_html_components as html
import mysql.connector
from dash.dependencies import Output, Input, State
from app import app
# from datetime import datetime
import datetime
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

#Connect to the MySQL database
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='admin',
    database='wrd_dash',
    auth_plugin='mysql_native_password'
)

def generate_station_link(station_type):
    # Generate the hyperlink using the station_id
    if station_type == 'ARG':
        url = '/arg'
    elif station_type == 'AWL':
        url = '/awlr'
    elif station_type == 'ARG+AWL':
        url = '/combine_stn'
    else:
        url = ''  # Default URL if station_id doesn't match any of the above

    return html.A(station_type, href=url)

def generate_download_link(data, filename):
    headers = ['Serial No.',
        'Station Id', 'Location', 'Station Types', 'Date Time',
        'Water Level(m)', 'Hourly_Rainfall(mm)', 'Daily_Rainfall(mm)',
        'Battery Voltage(v)', 'Solar Voltage(v)'
    ]
    csv_string = io.StringIO()
    csv_writer = csv.writer(csv_string)
    csv_writer.writerow(headers)
    for row in data:
        csv_writer.writerow(row)

    csv_string.seek(0)
    csv_bytes = csv_string.getvalue().encode()

    b64 = base64.b64encode(csv_bytes).decode()

    return html.Div([
        html.A(
            html.Button('Download', id='download-button', n_clicks=0),
            href='data:text/csv;base64,' + b64,
            download=filename
        )
    ], style={'margin-top': '10px'})

def update_table(n):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT id,stn_id, stn_location, stn_type, datetime, water_level_value, hourly_rainfall_value, daily_rainfall_value, battery_voltage, solar_voltage FROM realtime_data_update_table"
    )
    userdetails = cursor.fetchall()
    connection.commit()

    current_datetime = datetime.datetime.now()

    total_stations = len(userdetails)  # Total number of stations
    online_stations = sum(
        (current_datetime - userdetails[n][4]) < datetime.timedelta(hours=24) for n in range(total_stations)
    )  # Number of online stations
    offline_stations = total_stations - online_stations  # Number of offline stations

    table = html.Table(
        [
            html.Thead(
                html.Tr(
                    [
                        html.Th('Serial No.'),
                        html.Th('Station Id'),
                        html.Th('Location'),
                        html.Th('Station Types'),
                        html.Th('Date Time'),
                        html.Th('Water Level(m)'),
                        html.Th('Hourly_Rainfall(mm)'),
                        html.Th('Daily_Rainfall(mm)'),
                        html.Th('Battery Voltage(v)'),
                        html.Th('Solar Voltage(v)'),
                    ],
                    style={'background-color': 'lightgray'}
                )
            ),
            html.Tbody(
                [
                    html.Tr(
                        [
                            html.Td(row[0]),
                            html.Td(row[1]),
                            html.Td(row[2]),
                            html.Td(generate_station_link(row[3])),
                            html.Td(
                                row[4].strftime('%Y-%m-%d %H:%M:%S').replace('T', ' '),
                                style={'white-space': 'nowrap'}
                            ),
                            html.Td(row[5]),
                            html.Td(row[6]),
                            html.Td(row[7]),
                            html.Td(row[8]),
                            html.Td(row[9])
                        ],
                        id={'type': 'row', 'index': n},
                        style={
                            'height': '30px',
                            'background-color': 'orange' if (current_datetime - userdetails[n][4]) > datetime.timedelta(
                                hours=24) else 'white'
                        }
                    )
                    for n, row in enumerate(userdetails)
                ]
            ),
            html.Tr([
                html.Td(colSpan=9, children=[
                    generate_download_link(userdetails, 'data.csv')
                ])
            ])
        ], id='example', className='table table-striped table-bordered mt-2 my-table', style={'width': '100%'})

    return table

total_stn = dbc.Card(
    [
        dbc.CardHeader(html.H4('Total Station')),
        dbc.CardBody(html.H3(id='total-station-value')),
    ],
    className="text-center shadow my-4",
    style={'background-color': 'lightgray'}
)

offline_stn = dbc.Card(
    [
        dbc.CardHeader(html.H4('Offline Station')),
        dbc.CardBody(html.H3(id='offline-station-value')),
    ],
    className="text-center shadow my-4",
    style={'background-color': 'orange'}
)

online_stn = dbc.Card(
    [
        dbc.CardHeader(html.H4('Online Station')),
        dbc.CardBody(html.H3(id='online-station-value')),
    ],
    className="text-center shadow my-4",
)

layout = html.Div([
    dcc.Location(id='urlhome', refresh=True),
    html.H4('Real Time Data'),
    html.Hr(),
    html.Div([
        dbc.Container(
            dbc.Row(
                [
                    dbc.Col(total_stn),
                    dbc.Col(online_stn),
                    dbc.Col(offline_stn),
                ],
                className="mb-4",
            ),
            fluid=True,
        ),

        html.Div(id='table-container'),  # Include the table here
        dcc.Interval(id='interval-component', interval=60000, n_intervals=0)  # Interval component for refreshing the table
    ])
])

@app.callback(Output('total-station-value', 'children'),
              Output('online-station-value', 'children'),
              Output('offline-station-value', 'children'),
              Output('table-container', 'children'),
              Input('interval-component', 'n_intervals'))
def update_station_counts_and_table(n):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT stn_id, datetime FROM realtime_data_update_table")
    userdetails = cursor.fetchall()
    connection.commit()

    current_datetime = datetime.datetime.now()

    total_stations = len(userdetails)  # Total number of stations
    online_stations = sum((current_datetime - row[1]) < datetime.timedelta(hours=24) for row in userdetails)  # Number of online stations
    offline_stations = total_stations - online_stations  # Number of offline stations

    table = update_table(n)

    return total_stations, online_stations, offline_stations, table


