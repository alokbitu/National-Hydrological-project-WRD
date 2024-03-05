import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div(
        [
            html.Label('Station Type'),
            dcc.Input(id='input1', type='text'),
            html.Br(),
            html.Br(),
            html.Label('District'),
            dcc.Input(id='input2', type='text'),
            html.Br(),
            html.Br(),
            html.Label('River'),
            dcc.Input(id='input3', type='text'),
            html.Br(),
            html.Br(),
            html.Label('Basin'),
            dcc.Input(id='input4', type='text'),
        ],
        style={'width': '48%', 'display': 'inline-block'}
    ),
    html.Div(
        [
            html.Label('Location'),
            dcc.Input(id='input5', type='text'),
            html.Br(),
            html.Br(),
            html.Label('Longitude'),
            dcc.Input(id='input6', type='text'),
            html.Br(),
            html.Br(),
            html.Label('Latitude'),
            dcc.Input(id='input7', type='text'),
        ],
        style={'width': '48%', 'float': 'right', 'display': 'inline-block'}
    ),
    html.Br(),
    html.Br(),
    html.Button('Create Station Id', id='submit-button', n_clicks=0),
    html.Br(),
    html.Label(id='output')
])

@app.callback(Output('output', 'children'),
              [Input('submit-button', 'n_clicks')],
              [Input('input1', 'value'),
               Input('input2', 'value'),
               Input('input3', 'value'),
               Input('input4', 'value'),
               Input('input5', 'value'),
               Input('input6', 'value'),
               Input('input7', 'value')])
def update_output(n_clicks, input1, input2, input3, input4, input5, input6, input7):
    # Assign input values to Python variables
    var1 = input1
    var2 = input2
    var3 = input3
    var4 = input4
    var5 = input5
    var6 = input6
    var7 = input7
    # Set stationtype based on var1 value
    if var1 == "AWLR":
        stationtype = 1
    elif var1 == "ARS":
        stationtype = 2
    else:
        stationtype = 3
    print(var1,var2,var3,var4,var5,var6,var7,stationtype)

if __name__ == '__main__':
    app.run_server(debug=True)
