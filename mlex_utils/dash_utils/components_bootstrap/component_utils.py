import dash_bootstrap_components as dbc
from dash import html
from dash_iconify import DashIconify


class DbcControlItem(dbc.Row):
    """
    Customized layout for a control item
    """

    def __init__(self, title, title_id, item, style={"width": "100%", "margin": "0px"}):
        super(DbcControlItem, self).__init__(
            children=[
                dbc.Label(
                    title,
                    id=title_id,
                    size="sm",
                    style={
                        "width": "100%",
                        "align-content": "center",
                        "paddingRight": "5px",
                        "text-align": "right",
                    },
                ),
                html.Div(item, style={"width": "265px"}),
            ],
            style=style,
            className="g-0",
        )


def header(app_title, github_url, help_url, app_logo="assets/mlex.png"):
    """
    This header will exist at the top of the webpage rather than browser tab
    Args:
        app_title:      Title of dash app
        github_url:     URL to github repo
        help_url:       URL to help page
        app_logo:       URL to app logo
    """
    header = dbc.Navbar(
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            html.Img(
                                id="logo",
                                src=app_logo,
                                height="60px",
                            ),
                            md="auto",
                        ),
                        dbc.Col(
                            [
                                html.Div(
                                    [
                                        html.H3(
                                            app_title,
                                            style={
                                                "color": "white",
                                                "padding": "0px",
                                                "margin": "0px",
                                            },
                                        ),
                                    ],
                                    id="app-title",
                                )
                            ],
                            md=True,
                            align="center",
                        ),
                    ],
                    align="center",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.NavbarToggler(id="navbar-toggler"),
                                dbc.Collapse(
                                    dbc.Nav(
                                        [
                                            dbc.NavItem(
                                                dbc.NavLink(
                                                    DashIconify(
                                                        icon="mdi:github",
                                                        width=50,
                                                    ),
                                                    style={
                                                        "margin-right": "1rem",
                                                        "color": "#00313C",
                                                        "background-color": "white",
                                                    },
                                                    href=github_url,
                                                    active=True,
                                                )
                                            ),
                                            dbc.NavItem(
                                                dbc.NavLink(
                                                    DashIconify(
                                                        icon="mdi:help",
                                                        width=50,
                                                    ),
                                                    style={
                                                        "color": "#00313C",
                                                        "background-color": "white",
                                                    },
                                                    href=help_url,
                                                    active=True,
                                                )
                                            ),
                                        ],
                                        navbar=True,
                                        pills=True,
                                    ),
                                    id="navbar-collapse",
                                    navbar=True,
                                ),
                            ],
                            md=2,
                        ),
                    ],
                    align="center",
                ),
            ],
            fluid=True,
        ),
        dark=True,
        color="dark",
        sticky="top",
    )
    return header
