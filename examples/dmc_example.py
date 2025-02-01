import uuid

import dash_mantine_components as dmc
from dash import ALL, MATCH, Dash, Input, Output, callback, html
from dash_iconify import DashIconify
from models_utils import Models

from mlex_utils.dash_utils.components_mantime.component_utils import (
    DmcControlItem as ControlItem,
)
from mlex_utils.dash_utils.components_mantime.component_utils import (
    _accordion_item,
    _tooltip,
    drawer_section,
)
from mlex_utils.dash_utils.mlex_components import MLExComponents


def layout(job_manager):
    """
    Returns the layout for the control panel in the app UI
    """
    return drawer_section(
        "MLExchange Utils Example with DMC",
        dmc.Stack(
            style={"width": "400px"},
            children=[
                dmc.AccordionMultiple(
                    id="control-accordion",
                    value=["data-select", "image-transformations", "run-model"],
                    children=[
                        _accordion_item(
                            "Data selection",
                            "majesticons:data-line",
                            "data-select",
                            id="data-selection-controls",
                            children=[
                                dmc.Space(h=5),
                                ControlItem(
                                    "Dataset",
                                    "image-selector",
                                    dmc.Grid(
                                        [
                                            dmc.Select(
                                                id="project-name-src",
                                                data=[],
                                                placeholder="Select an image to view...",
                                            ),
                                            dmc.ActionIcon(
                                                _tooltip(
                                                    "Refresh dataset",
                                                    children=[
                                                        DashIconify(
                                                            icon="mdi:refresh-circle",
                                                            width=20,
                                                        ),
                                                    ],
                                                ),
                                                size="xs",
                                                variant="subtle",
                                                id="refresh-tiled",
                                                n_clicks=0,
                                                style={"margin": "auto"},
                                            ),
                                        ],
                                        style={"margin": "0px"},
                                    ),
                                ),
                                dmc.Space(h=10),
                            ],
                        ),
                        _accordion_item(
                            "Image transformations",
                            "fluent-mdl2:image-pixel",
                            "image-transformations",
                            id="image-transformation-controls",
                            children=html.Div(
                                [
                                    dmc.Space(h=5),
                                    ControlItem(
                                        "Brightness",
                                        "bightness-text",
                                        [
                                            dmc.Grid(
                                                [
                                                    dmc.Slider(
                                                        id={
                                                            "type": "slider",
                                                            "index": "brightness",
                                                        },
                                                        value=100,
                                                        min=0,
                                                        max=255,
                                                        step=1,
                                                        color="gray",
                                                        size="sm",
                                                        style={"width": "225px"},
                                                    ),
                                                    dmc.ActionIcon(
                                                        _tooltip(
                                                            "Reset brightness",
                                                            children=[
                                                                DashIconify(
                                                                    icon="fluent:arrow-reset-32-regular",
                                                                    width=15,
                                                                ),
                                                            ],
                                                        ),
                                                        size="xs",
                                                        variant="subtle",
                                                        id={
                                                            "type": "reset",
                                                            "index": "brightness",
                                                        },
                                                        n_clicks=0,
                                                        style={"margin": "auto"},
                                                    ),
                                                ],
                                                style={"margin": "0px"},
                                            )
                                        ],
                                    ),
                                    dmc.Space(h=20),
                                    ControlItem(
                                        "Contrast",
                                        "contrast-text",
                                        dmc.Grid(
                                            [
                                                dmc.Slider(
                                                    id={
                                                        "type": "slider",
                                                        "index": "contrast",
                                                    },
                                                    value=100,
                                                    min=0,
                                                    max=255,
                                                    step=1,
                                                    color="gray",
                                                    size="sm",
                                                    style={"width": "225px"},
                                                ),
                                                dmc.ActionIcon(
                                                    _tooltip(
                                                        "Reset contrast",
                                                        children=[
                                                            DashIconify(
                                                                icon="fluent:arrow-reset-32-regular",
                                                                width=15,
                                                            ),
                                                        ],
                                                    ),
                                                    size="xs",
                                                    variant="subtle",
                                                    id={
                                                        "type": "reset",
                                                        "index": "contrast",
                                                    },
                                                    n_clicks=0,
                                                    style={"margin": "auto"},
                                                ),
                                            ],
                                            style={"margin": "0px"},
                                        ),
                                    ),
                                    dmc.Space(h=10),
                                ]
                            ),
                        ),
                        _accordion_item(
                            "Model configuration",
                            "carbon:ibm-watson-machine-learning",
                            "run-model",
                            id="model-configuration",
                            children=job_manager,
                        ),
                    ],
                ),
            ],
        ),
    )


# Get models
models = Models(modelfile_path="./examples/assets/models_dmc.json")

# Get MLExchange dash components
mlex_components = MLExComponents("dmc")
job_manager = mlex_components.get_job_manager(model_list=models.modelname_list)

app = Dash(__name__)
app.layout = dmc.MantineProvider(
    theme={"colorScheme": "light"},
    children=[
        layout(job_manager),
        html.Div(
            id="model-params-out",
            style={"margin-left": "450px"},
        ),
    ],
)


@callback(
    Output(
        {
            "component": "DmcJobManagerAIO",
            "subcomponent": "model-parameters",
            "aio_id": MATCH,
        },
        "children",
    ),
    Input(
        {
            "component": "DmcJobManagerAIO",
            "subcomponent": "model-list",
            "aio_id": MATCH,
        },
        "value",
    ),
)
def update_model_parameters(model_name):
    model = models[model_name]
    if model["gui_parameters"]:
        item_list = mlex_components.get_parameter_items(
            _id={"type": str(uuid.uuid4())}, json_blob=model["gui_parameters"]
        )
        return item_list
    else:
        return html.Div("Model has no parameters")


@callback(
    Output("model-params-out", "children"),
    Input(
        {
            "component": "DmcJobManagerAIO",
            "subcomponent": "model-parameters",
            "aio_id": ALL,
        },
        "children",
    ),
    prevent_initial_call=True,
)
def update_model_parameters_output(model_parameter_container):
    model_parameters, parameter_errors = mlex_components.get_parameters_values(
        model_parameter_container[0]
    )
    return str(model_parameters)


if __name__ == "__main__":
    app.run_server(debug=True, port=8051)
