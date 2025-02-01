import uuid

import dash_mantine_components as dmc
from dash import MATCH, Input, Output, State, callback, dcc
from dash_iconify import DashIconify


class DmcAdvancedOptionsAIO(dmc.Modal):

    class ids:

        advanced_options_modal = lambda aio_id: {  # noqa: E731
            "component": "DmcAdvancedOptionsAIO",
            "subcomponent": "advanced-options-modal",
            "aio_id": aio_id,
        }

        cancel_button = lambda aio_id: {  # noqa: E731
            "component": "DmcAdvancedOptionsAIO",
            "subcomponent": "cancel-button",
            "aio_id": aio_id,
        }

        delete_button = lambda aio_id: {  # noqa: E731
            "component": "DmcAdvancedOptionsAIO",
            "subcomponent": "delete-button",
            "aio_id": aio_id,
        }

        logs_area = lambda aio_id: {  # noqa: E731
            "component": "DmcAdvancedOptionsAIO",
            "subcomponent": "logs-area",
            "aio_id": aio_id,
        }

        job_id = lambda aio_id: {  # noqa: E731
            "component": "DmcAdvancedOptionsAIO",
            "subcomponent": "job-id",
            "aio_id": aio_id,
        }

        warning_delete_modal = lambda aio_id: {  # noqa: E731
            "component": "DmcAdvancedOptionsAIO",
            "subcomponent": "warning-delete-modal",
            "aio_id": aio_id,
        }

        warning_cancel_modal = lambda aio_id: {  # noqa: E731
            "component": "DmcAdvancedOptionsAIO",
            "subcomponent": "warning-cancel-modal",
            "aio_id": aio_id,
        }

        warning_confirm_delete = lambda aio_id: {  # noqa: E731
            "component": "DmcAdvancedOptionsAIO",
            "subcomponent": "warning-confirm-delete",
            "aio_id": aio_id,
        }

        warning_confirm_cancel = lambda aio_id: {  # noqa: E731
            "component": "DmcAdvancedOptionsAIO",
            "subcomponent": "warning-confirm-cancel",
            "aio_id": aio_id,
        }

        warning_undo_delete = lambda aio_id: {  # noqa: E731
            "component": "DmcAdvancedOptionsAIO",
            "subcomponent": "warning-undo-delete",
            "aio_id": aio_id,
        }

        warning_undo_cancel = lambda aio_id: {  # noqa: E731
            "component": "DmcAdvancedOptionsAIO",
            "subcomponent": "warning-undo-cancel",
            "aio_id": aio_id,
        }

    ids = ids

    def __init__(
        self,
        cancel_button_props=None,
        delete_button_props=None,
        logs_area_props=None,
        aio_id=None,
    ):
        """
        JobExecutionAIO is an All-in-One component that is composed
        of a parent `html.Div` with a button to cancel, delete, and advance a job.
        - `cancel_button_props` - A dictionary of properties passed into the Button component for the cancel button.
        - `delete_button_props` - A dictionary of properties passed into the Button component for the delete button.
        - `logs_area_props` - A dictionary of properties passed into the Textarea component for the logs area.
        - `aio_id` - The All-in-One component ID used to generate the markdown and dropdown components's dictionary IDs.
        """
        if aio_id is None:
            aio_id = str(uuid.uuid4())

        cancel_button_props = self._update_button_props(cancel_button_props)
        delete_button_props = self._update_button_props(delete_button_props)

        super().__init__(
            title="Advanced Options",
            id=self.ids.advanced_options_modal(aio_id),
            opened=False,
            children=[
                dmc.ScrollArea(
                    children=dmc.Paper(
                        [
                            dmc.Text(
                                "These are the logs...",
                                id=self.ids.logs_area(aio_id),
                            ),
                        ],
                        style={"width": "100%", "height": 200, "margin-bottom": "10px"},
                    ),
                ),
                dmc.Accordion(
                    children=[
                        dmc.AccordionItem(
                            [
                                dmc.AccordionControl(
                                    "Danger Zone",
                                    icon=DashIconify(
                                        icon="mdi:alert-circle",
                                        # color=dmc.DEFAULT_THEME["colors"]["red"][6],
                                        width=20,
                                    ),
                                ),
                                dmc.AccordionPanel(
                                    [
                                        dmc.Grid(
                                            [
                                                dmc.Col(
                                                    dmc.Button(
                                                        "Cancel Job",
                                                        id=self.ids.cancel_button(
                                                            aio_id
                                                        ),
                                                        **cancel_button_props,
                                                    ),
                                                    span=6,
                                                ),
                                                dmc.Col(
                                                    dmc.Button(
                                                        "Delete Job",
                                                        id=self.ids.delete_button(
                                                            aio_id
                                                        ),
                                                        **delete_button_props,
                                                    ),
                                                    span=6,
                                                ),
                                            ]
                                        ),
                                    ],
                                ),
                            ],
                            value="danger_zone",
                        ),
                    ],
                ),
                dcc.Store(id=self.ids.job_id(aio_id), data=None),
                dmc.Modal(
                    title="Warning",
                    id=self.ids.warning_cancel_modal(aio_id),
                    opened=False,
                    children=[
                        dmc.Text("Are you sure you want to cancel this job?"),
                        dmc.Space(h=25),
                        dmc.Grid(
                            [
                                dmc.Col(
                                    dmc.Button(
                                        "YES",
                                        id=self.ids.warning_confirm_cancel(aio_id),
                                        color="red",
                                        style={"width": "100%", "margin": "5px"},
                                    ),
                                    span=6,
                                ),
                                dmc.Col(
                                    dmc.Button(
                                        "NO",
                                        id=self.ids.warning_undo_cancel(aio_id),
                                        style={"width": "100%", "margin": "5px"},
                                    ),
                                    span=6,
                                ),
                            ]
                        ),
                    ],
                ),
                dmc.Modal(
                    title="Warning",
                    id=self.ids.warning_delete_modal(aio_id),
                    opened=False,
                    children=[
                        dmc.Text("Are you sure you want to delete this job?"),
                        dmc.Space(h=25),
                        dmc.Grid(
                            [
                                dmc.Col(
                                    dmc.Button(
                                        "YES",
                                        id=self.ids.warning_confirm_delete(aio_id),
                                        variant="light",
                                        color="red",
                                        style={"width": "100%", "margin": "5px"},
                                    ),
                                    span=6,
                                ),
                                dmc.Col(
                                    dmc.Button(
                                        "NO",
                                        id=self.ids.warning_undo_delete(aio_id),
                                        variant="light",
                                        style={"width": "100%", "margin": "5px"},
                                    ),
                                    span=6,
                                ),
                            ]
                        ),
                    ],
                ),
            ],
        )

    def _update_button_props(
        self,
        button_props,
        variant="light",
        color="red",
        style={"width": "100%", "margin": "5px"},
    ):
        button_props = button_props.copy() if button_props else {}
        button_props["variant"] = (
            variant if "variant" not in button_props else button_props["variant"]
        )
        button_props["color"] = (
            color if "color" not in button_props else button_props["color"]
        )
        button_props["style"] = (
            style if "style" not in button_props else button_props["style"]
        )
        return button_props

    @staticmethod
    @callback(
        Output(ids.warning_cancel_modal(MATCH), "opened"),
        Input(ids.cancel_button(MATCH), "n_clicks"),
        Input(ids.warning_undo_cancel(MATCH), "n_clicks"),
        Input(ids.warning_confirm_cancel(MATCH), "n_clicks"),
        State(ids.warning_cancel_modal(MATCH), "opened"),
        prevent_initial_call=True,
    )
    def toggle_warning_cancel_modal(
        cancel_button_n_clicks,
        undo_cancel_button_n_clicks,
        confirm_cancel_button_n_clicks,
        is_open,
    ):
        return not is_open

    @staticmethod
    @callback(
        Output(ids.warning_delete_modal(MATCH), "opened"),
        Input(ids.delete_button(MATCH), "n_clicks"),
        Input(ids.warning_undo_delete(MATCH), "n_clicks"),
        Input(ids.warning_confirm_delete(MATCH), "n_clicks"),
        State(ids.warning_delete_modal(MATCH), "opened"),
        prevent_initial_call=True,
    )
    def toggle_warning_delete_modal(
        delete_button_n_clicks,
        undo_delete_button_n_clicks,
        confirm_delete_n_clicks,
        is_open,
    ):
        return not is_open
