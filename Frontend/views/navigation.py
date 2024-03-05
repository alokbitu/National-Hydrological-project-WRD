import dash_bootstrap_components as dbc
# import dash_html_components as html
from dash import html
from app import app
from dash.dependencies import Input, Output, State
import dash

navbar = dbc.Navbar(

    dbc.Container(
        [
            dbc.Row([
                dbc.Col([
                    html.Img(src=dash.get_asset_url('logo2.png'), height="40px"),
                    dbc.NavbarBrand("Water Inlet Project", className="ms-2")
                ],
                    width={"size": "auto"})
            ],
                #children=[],
                align="center",
                className="g-0")
         ],

    ),

    sticky='top',
    color='primary',
    className='navbar navbar-expand-lg navbar-dark bg-primary',
)


@dash.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open