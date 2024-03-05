# index page
import dash_core_components as dcc
import dash_html_components as html
import dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from app import app, server
from flask_login import logout_user, current_user
from views import login, error, home, realtime_data_query, battery_voltage, arg, awlr, combine_stn, Historical
from views.navigation import navbar

navBar = dbc.Navbar(id='navBar',
    children=[],

    sticky='top',
    color='success',
    className='navbar navbar-expand-lg navbar-light',
)


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        navBar,
        html.Div(id='pageContent')
    ],id='container1')
], id='table-wrapper')


################################################################################
# HANDLE PAGE ROUTING - IF USER NOT LOGGED IN, ALWAYS RETURN TO LOGIN SCREEN
################################################################################
@app.callback(Output('pageContent', 'children'),
              [Input('url', 'pathname')])
def displayPage(pathname):
    if pathname == '/':
        if current_user.is_authenticated:
            return home.layout
        else:
            return login.layout

    elif pathname == '/logout':
        if current_user.is_authenticated:
            logout_user()
            return login.layout
        else:
            return login.layout

    if pathname == '/home' or pathname == '/page1':
        if current_user.is_authenticated:
            return home.layout
        else:
            return login.layout

    if pathname == '/realtime_data_query':
        if current_user.is_authenticated:
            return realtime_data_query.layout
        else:
            return login.layout

    if pathname == '/battery_voltage':
        if current_user.is_authenticated:
            return battery_voltage.layout
        else:
            return login.layout
    if pathname == '/arg':
        if current_user.is_authenticated:
            return arg.layout
        else:
            return login.layout
    if pathname == '/awlr':
        if current_user.is_authenticated:
            return awlr.layout
        else:
            return login.layout
    if pathname == '/combine_stn':
        if current_user.is_authenticated:
            return combine_stn.layout
        else:
            return login.layout
    if pathname == '/Historical':
        if current_user.is_authenticated:
            return Historical.layout
        else:
            return login.layout

################################################################################
# ONLY SHOW NAVIGATION BAR WHEN A USER IS LOGGED IN
################################################################################
@app.callback(
    Output('navBar', 'children'),
    [Input('pageContent', 'children')])
def navBar(input1):
    if current_user.is_authenticated:
        if current_user.admin == 1:
            navBarContents = [
                dbc.Container([
                    html.Div(html.Img(src=app.get_asset_url("wrd.jpg"), className="logo-image"),
            className="logo-container"),
                    # html.Img(src=app.get_asset_url("wrd.jpg"), style={"height": "50px", "object-fit": "contain"}),
                    dbc.Row([
                        dbc.Col([
                            html.H1("Hydromet RTDAS,Odisha", style={"textAlign": "center"}),
                        ])
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Nav([
                                dbc.NavItem(dbc.NavLink('Home', href='/home')),
                                # dbc.NavItem(dbc.NavLink('About Us', href='/about-us')),
                                # dbc.NavItem(dbc.NavLink('Dashboard', href='/dashboard')),
                                dbc.NavItem(
                                    dbc.DropdownMenu(
                                        nav=True,
                                        in_navbar=True,
                                        label='Hydrological Data',
                                        children=[
                                            dbc.DropdownMenuItem('Real-time Data query', href='/realtime_data_query'),
                                            dbc.DropdownMenuItem('Battery Voltage', href='/battery_voltage'),
                                            dbc.DropdownMenuItem('Rainfall(ARG)', href='/arg'),
                                            dbc.DropdownMenuItem('Water Level(AWLR)', href='/awlr'),
                                            dbc.DropdownMenuItem('Rainfall/WaterLevel(ARG+AWLR)', href='/combine_stn'),
                                        ],
                                    )
                                ),
                                dbc.NavItem(dbc.NavLink('Historical', href='/Historical')),
                                dbc.DropdownMenu(
                                    nav=True,
                                    in_navbar=True,
                                    label=current_user.username,
                                    children=[
                                        dbc.DropdownMenuItem('Logout', href='/logout'),
                                    ],
                                ),
                            ]),
                        ])
                    ]),
                ],fluid=True)
            ]
            return navBarContents

        else:
            navBarContents = [
                dbc.Container([
                    html.Img(src=app.get_asset_url("wrd.jpg"), height="50px",style={"border": "none"}),
                    dbc.Row([
                        dbc.Col([
                            html.H2("Hydromet RTDAS,Odisha", style={"textAlign": "center"}),
                        ])
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Nav([
                                dbc.NavItem(dbc.NavLink('Home', href='/home')),
                                # dbc.NavItem(dbc.NavLink('About Us', href='/about-us')),
                                # dbc.NavItem(dbc.NavLink('Dashboard', href='/dashboard')),
                                dbc.NavItem(
                                    dbc.DropdownMenu(
                                        nav=True,
                                        in_navbar=True,
                                        label='Hydrological Data',
                                        children=[
                                            dbc.DropdownMenuItem('Real-time Data query', href='/realtime_data_query'),
                                            dbc.DropdownMenuItem('Battery Voltage', href='/battery_voltage'),
                                            dbc.DropdownMenuItem('Rainfall(ARG)', href='/arg'),
                                            dbc.DropdownMenuItem('Water Level(AWLR)', href='/awlr'),
                                            dbc.DropdownMenuItem('Rainfall/WaterLevel(ARG+AWLR)', href='/combine_stn'),
                                        ],
                                    )
                                ),
                                dbc.NavItem(dbc.NavLink('Historical', href='/Historical')),
                                dbc.DropdownMenu(
                                    nav=True,
                                    in_navbar=True,
                                    label=current_user.username,
                                    children=[
                                        dbc.DropdownMenuItem('Logout', href='/logout'),
                                    ],
                                ),
                            ]),
                        ])
                    ]),
                ],fluid=True)
            ]
            return navBarContents
    else:
        return ''



if __name__ == '__main__':
    app.run_server(debug=True,host='localhost', port = 3307)
    # app.run_server(debug=True)
