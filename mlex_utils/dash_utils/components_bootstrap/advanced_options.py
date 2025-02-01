import uuid

import dash_bootstrap_components as dbc
from dash import MATCH, Input, Output, State, callback, dcc


class DbcAdvancedOptionsAIO(dbc.Modal):

    class ids:

        advanced_options_modal = lambda aio_id: {  # noqa: E731
            "component": "DbcAdvancedOptionsAIO",
            "subcomponent": "advanced-options-modal",
            "aio_id": aio_id,
        }

        cancel_button = lambda aio_id: {  # noqa: E731
            "component": "DbcAdvancedOptionsAIO",
            "subcomponent": "cancel-button",
            "aio_id": aio_id,
        }

        delete_button = lambda aio_id: {  # noqa: E731
            "component": "DbcAdvancedOptionsAIO",
            "subcomponent": "delete-button",
            "aio_id": aio_id,
        }

        logs_area = lambda aio_id: {  # noqa: E731
            "component": "DbcAdvancedOptionsAIO",
            "subcomponent": "logs-area",
            "aio_id": aio_id,
        }

        job_id = lambda aio_id: {  # noqa: E731
            "component": "DbcAdvancedOptionsAIO",
            "subcomponent": "job-id",
            "aio_id": aio_id,
        }

        warning_delete_modal = lambda aio_id: {  # noqa: E731
            "component": "DbcAdvancedOptionsAIO",
            "subcomponent": "warning-delete-modal",
            "aio_id": aio_id,
        }

        warning_cancel_modal = lambda aio_id: {  # noqa: E731
            "component": "DbcAdvancedOptionsAIO",
            "subcomponent": "warning-cancel-modal",
            "aio_id": aio_id,
        }

        warning_confirm_delete = lambda aio_id: {  # noqa: E731
            "component": "DbcAdvancedOptionsAIO",
            "subcomponent": "warning-confirm-delete",
            "aio_id": aio_id,
        }

        warning_confirm_cancel = lambda aio_id: {  # noqa: E731
            "component": "DbcAdvancedOptionsAIO",
            "subcomponent": "warning-confirm-cancel",
            "aio_id": aio_id,
        }

        warning_undo_delete = lambda aio_id: {  # noqa: E731
            "component": "DbcAdvancedOptionsAIO",
            "subcomponent": "warning-undo-delete",
            "aio_id": aio_id,
        }

        warning_undo_cancel = lambda aio_id: {  # noqa: E731
            "component": "DbcAdvancedOptionsAIO",
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

        cancel_button_props, delete_button_props = self._update_props(
            cancel_button_props, delete_button_props
        )

        super().__init__(
            id=self.ids.advanced_options_modal(aio_id),
            children=[
                dbc.ModalHeader("Advanced Options"),
                dbc.ModalBody(id=self.ids.logs_area(aio_id)),
                dbc.ModalFooter(
                    dbc.Accordion(
                        dbc.AccordionItem(
                            title="Danger Zone",
                            children=dbc.Row(
                                [
                                    dbc.Col(
                                        dbc.Button(
                                            "Cancel Job",
                                            id=self.ids.cancel_button(aio_id),
                                            **cancel_button_props,
                                        ),
                                    ),
                                    dbc.Col(
                                        dbc.Button(
                                            "Delete Job",
                                            id=self.ids.delete_button(aio_id),
                                            **delete_button_props,
                                        ),
                                    ),
                                ],
                            ),
                        ),
                        start_collapsed=True,
                        flush=True,
                        style={"width": "100%", "--bs-accordion-active-bg": "#ffb3b3"},
                    ),
                ),
                dcc.Store(id=self.ids.job_id(aio_id), data=None),
                dbc.Modal(
                    id=self.ids.warning_cancel_modal(aio_id),
                    children=[
                        dbc.ModalHeader("Warning"),
                        dbc.ModalBody("Are you sure you want to cancel this job?"),
                        dbc.ModalFooter(
                            [
                                dbc.Button(
                                    "YES",
                                    id=self.ids.warning_confirm_cancel(aio_id),
                                    color="danger",
                                    className="ml-auto",
                                ),
                                dbc.Button(
                                    "NO",
                                    id=self.ids.warning_undo_cancel(aio_id),
                                    className="ml-auto",
                                ),
                            ]
                        ),
                    ],
                ),
                dbc.Modal(
                    id=self.ids.warning_delete_modal(aio_id),
                    children=[
                        dbc.ModalHeader("Warning"),
                        dbc.ModalBody("Are you sure you want to delete this job?"),
                        dbc.ModalFooter(
                            [
                                dbc.Button(
                                    "YES",
                                    id=self.ids.warning_confirm_delete(aio_id),
                                    color="danger",
                                    className="ml-auto",
                                ),
                                dbc.Button(
                                    "NO",
                                    id=self.ids.warning_undo_delete(aio_id),
                                    className="ml-auto",
                                ),
                            ]
                        ),
                    ],
                ),
            ],
            scrollable=True,
            size="lg",
        )

    def _update_props(self, cancel_button_props, delete_button_props):
        cancel_button_props = cancel_button_props.copy() if cancel_button_props else {}
        delete_button_props = delete_button_props.copy() if delete_button_props else {}

        cancel_button_props = self._update_button_props(
            cancel_button_props, "danger", {"width": "100%"}
        )
        delete_button_props = self._update_button_props(
            delete_button_props, "danger", {"width": "100%"}
        )
        return cancel_button_props, delete_button_props

    def _update_button_props(self, button_props, color, style):
        button_props["color"] = color
        button_props["style"] = style
        return button_props

    @staticmethod
    @callback(
        Output(ids.warning_cancel_modal(MATCH), "is_open"),
        Input(ids.cancel_button(MATCH), "n_clicks"),
        Input(ids.warning_undo_cancel(MATCH), "n_clicks"),
        State(ids.warning_cancel_modal(MATCH), "is_open"),
        prevent_initial_call=True,
    )
    def toggle_warning_cancel_modal(
        cancel_button_n_clicks, undo_cancel_button_n_clicks, is_open
    ):
        return not is_open

    @staticmethod
    @callback(
        Output(ids.warning_delete_modal(MATCH), "is_open"),
        Input(ids.delete_button(MATCH), "n_clicks"),
        Input(ids.warning_undo_delete(MATCH), "n_clicks"),
        State(ids.warning_delete_modal(MATCH), "is_open"),
        prevent_initial_call=True,
    )
    def toggle_warning_delete_modal(
        delete_button_n_clicks, undo_delete_button_n_clicks, is_open
    ):
        return not is_open
