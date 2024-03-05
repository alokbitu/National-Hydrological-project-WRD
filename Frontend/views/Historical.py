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
from dash.dependencies import Input, Output, State
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
layout = html.Div([
dcc.Location(id='urlhist', refresh=True),
    html.H4('Historical Page'),
    html.Hr(),
    dbc.Row([
        dbc.Col([dcc.Dropdown(
            id='field-dropdown6',
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
                id='location-dropdown6',
                options=[],
                placeholder="Location"
            ),
        ]),
        dbc.Col([dcc.Dropdown(
            id='station-dropdown6',
            options=[],
            placeholder="Station ID"
        ),
        ])
    ]),
    dbc.Row([
        dbc.Col([dcc.DatePickerRange(
            id='date-range-picker',
            start_date_placeholder_text='Start Date',
            end_date_placeholder_text='End Date',
            calendar_orientation='horizontal',
            clearable=True,
            style={
                'background-color': 'lightgray',
                'border': '1px solid gray',
                'border-radius': '5px',
                'padding': '5px',
                'color': 'black',
                'font-size': '14px',
                'width': '300px',

            }
    )],style={'margin': '20px'},width=2),
        ],className="mt-2"),
    dbc.Row([
        dbc.Col([html.Button('Chart View', id='chart-button6', n_clicks=0),
                 html.Div(id='output-container6'),
                 html.Div(id='graph-container6'),
                 dcc.Store(id='data-store6'),
                 ],width=5),
        dbc.Col([
            html.Button('Table View', id='table-button6', n_clicks=0),

            html.Button('Report Download', id='report-button6', n_clicks=0),
            dcc.Download(id='download-report6'),
            html.Div(id='table-container6'),
            html.Div(id='report-container6'),
            dcc.Interval(
                id='report_interval-component6',
                interval=60000,  # 1 minute in milliseconds
                n_intervals=0
            )
        ],width=5),
    ],className="mt-2")
])
@app.callback(
    Output('location-dropdown6', 'options'),
    [Input('field-dropdown6', 'value')]
)
def update_location_options(field):
    if field is not None:
        cursor.execute("SELECT DISTINCT stn_location FROM stn_master WHERE stn_type = %s", (field,))
        location_options = [{'label': stn_location, 'value': stn_location} for stn_location, in cursor.fetchall()]
        return location_options
    return []

@app.callback(
    dash.dependencies.Output('station-dropdown6', 'options'),
    [dash.dependencies.Input('field-dropdown6', 'value'),
     dash.dependencies.Input('location-dropdown6', 'value')]
)
def update_station_options(field, stn_location):
    if field is not None and stn_location is not None:
        cursor.execute("SELECT DISTINCT stn_id FROM stn_master WHERE stn_type = %s AND stn_location = %s", (field, stn_location))
        station_options = [{'label': stn_id, 'value': stn_id} for stn_id, in cursor.fetchall()]
        return station_options
    return []

@app.callback(
    Output('table-container6', 'children'),
    [Input('station-dropdown6', 'value'),
     Input('field-dropdown6', 'value'),
     Input('table-button6', 'n_clicks'),
     Input('report_interval-component6', 'n_intervals'),
     State('date-range-picker', 'start_date'),
     State('date-range-picker', 'end_date')

]
)
def display_table(stn_id, field, table_clicks, n_intervals, start_date, end_date):
    if table_clicks is not None and table_clicks > 0 and stn_id is not None and field is not None and start_date is not None and end_date is not None:
        print(stn_id,field,start_date,end_date)
        cursor.execute("SELECT datetime, hourly_rainfall_value, daily_rainfall_value, water_level_value, battery_voltage, solar_voltage FROM realtime_data_query_table WHERE stn_id = %s AND stn_type = %s AND datetime BETWEEN %s AND %s", (stn_id, field, start_date, end_date))
        rows = cursor.fetchall()
        list_of_lists = [[str(item) for item in tpl] for tpl in rows]
        if len(rows) == 0:
            return 'No information found for station {} in field {}'.format(stn_id, field)
        else:
            headers = ['DATE & TIME', 'Hr_Rain Fall(mm)','Daily_Rain Fall(mm)', 'Water Level(m)', 'Battery Voltage(V)', 'Solar Voltage(V)']

            table = html.Div([
                html.Table(
                    [html.Tr([html.Th(col) for col in headers],
                             style={'background-color': '#D5DBDB', 'padding': '20px 1px'})] +
                    [html.Tr([html.Td(str(cell).replace('T', ' ')) for cell in row],
                             style={'padding': '10px', 'font-size': '12px'}) for row in rows],
                    style={'border-collapse': 'collapse', 'margin-bottom': '20px', 'font-size': '12px'}
                )
            ], id='table-container6')
            return table
    return html.Div()

@app.callback(
    dash.dependencies.Output('data-store6', 'data'),
    [dash.dependencies.Input('station-dropdown6', 'value'),
     dash.dependencies.Input('field-dropdown6', 'value'),
     dash.dependencies.Input('date-range-picker', 'start_date'),
     dash.dependencies.Input('date-range-picker', 'end_date')]
)
def update_data_store(stn_id, field, start_date, end_date):
    if stn_id is not None and field is not None:
        cursor.execute("SELECT datetime, hourly_rainfall_value, daily_rainfall_value, water_level_value, battery_voltage, solar_voltage FROM realtime_data_query_table WHERE stn_id = %s AND stn_type = %s AND datetime >= %s AND datetime <= %s", (stn_id, field, start_date, end_date))
        rows = cursor.fetchall()
        if len(rows) == 0:
            return None
        else:
            headers = ['DATE & TIME', 'Hr_Rain Fall(mm)','Daily_Rain Fall(mm)','Water Level(m)', 'Battery Voltage(V)', 'Solar Voltage(V)']
            list_of_lists = [[str(item) for item in tpl] for tpl in rows]

            # Store the filtered data (rows) along with headers in a variable
            filtered_data = [headers] + list_of_lists

            return filtered_data
            # data = [headers]
            # for row in rows:
            #     data.append([str(item) for item in row])
            # return data
    return None

@app.callback(
    Output('graph-container6', 'children'),
    [Input('chart-button6', 'n_clicks')],
    [State('data-store6', 'data')]
)
def display_graph(n_clicks, data):
    if n_clicks > 0 and data is not None:
        headers = data[0]
        list_of_lists = data[1:]
        headers = data[0]
        list_of_lists = data[1:]

        df = pd.DataFrame(list_of_lists, columns=headers)
        fig = px.line(df, x='DATE & TIME', y=df.columns[1:], title='Station Data', markers=True)

        graph = dcc.Graph(id='station-graph', figure=fig)
        return graph
    return ''

@app.callback(
    [Output('download-report6', 'data'), Output('report-container6', 'children')],
    [Input('station-dropdown6', 'value'),
     Input('field-dropdown6', 'value'),
     Input('report-button6', 'n_clicks')],
     State('date-range-picker', 'start_date'),
     State('date-range-picker', 'end_date')
)
def download_report(stn_id, field, report_clicks, start_date, end_date):
    if report_clicks is not None and report_clicks > 0 and stn_id is not None and field is not None and start_date is not None and end_date is not None:
        cursor.execute("SELECT datetime, hourly_rainfall_value, daily_rainfall_value, water_level_value, battery_voltage, solar_voltage FROM realtime_data_query_table WHERE stn_id = %s AND stn_type = %s AND datetime BETWEEN %s AND %s", (stn_id, field, start_date, end_date))

        rows = cursor.fetchall()
        headers = ['DATE & TIME', 'Hr_Rain Fall(mm)', 'Daily_Rain Fall(mm)', 'Water Level(m)', 'Battery Voltage(V)', 'Solar Voltage(V)']
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
