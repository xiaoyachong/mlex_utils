import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify


class DmcControlItem(dmc.Grid):
    """
    Customized layout for a control item
    """

    def __init__(self, title, title_id, item, style={}):
        super(DmcControlItem, self).__init__(
            children=[
                dmc.Text(
                    title,
                    id=title_id,
                    size="sm",
                    style={"width": "100px", "margin": "auto", "paddingRight": "5px"},
                    align="right",
                ),
                html.Div(item, style={"width": "265px", "margin": "auto"}),
            ],
            style=style,
        )


def _accordion_item(title, icon, value, children, id):
    """
    Returns a customized layout for an accordion item
    """
    panel = dmc.AccordionPanel(children=children, id=id)
    return dmc.AccordionItem(
        [
            dmc.AccordionControl(
                title,
                icon=DashIconify(
                    icon=icon,
                    color="#00313C",
                    width=20,
                ),
            ),
            panel,
        ],
        value=value,
    )


def _tooltip(text, children):
    """
    Returns a customized layout for a tooltip
    """
    return dmc.Tooltip(
        label=text, withArrow=True, position="top", color="#464646", children=children
    )


def drawer_section(title, children):
    """
    This components creates an affix button that opens a drawer with the given children.
    Drawer is set to have height and width of fit-content, meaning it won't be full height.
    """
    return html.Div(
        [
            dmc.Affix(
                dmc.Button(
                    [
                        DashIconify(
                            icon="circum:settings",
                            height=25,
                            style={"cursor": "pointer"},
                        ),
                        dmc.Text("Controls", size="sm"),
                    ],
                    id="drawer-controls-open-button",
                    size="lg",
                    radius="sm",
                    compact=True,
                    variant="outline",
                    color="gray",
                ),
                position={"left": "25px", "top": "25px"},
            ),
            dmc.Drawer(
                title=dmc.Text(title, weight=700),
                id="drawer-controls",
                padding="md",
                transition="fade",
                transitionDuration=500,
                shadow="md",
                withOverlay=False,
                position="left",
                zIndex=10000,
                styles={
                    "drawer": {
                        "width": "fit-content",
                        "height": "fit-content",
                        "max-height": "100%",
                        "overflow-y": "auto",
                        "margin": "0px",
                    },
                    "root": {
                        "opacity": "0.95",
                    },
                },
                children=children,
                opened=True,
            ),
        ]
    )
