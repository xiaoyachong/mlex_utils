import uuid

import dash_mantine_components as dmc
from dash import MATCH, Input, Output, State, callback, dcc, html
from dash_iconify import DashIconify

from mlex_utils.dash_utils.callbacks.manage_jobs import (
    _cancel_job,
    _check_inference_job,
    _check_train_job,
    _delete_job,
    _get_job_logs,
)
from mlex_utils.dash_utils.components_mantime.advanced_options import (
    DmcAdvancedOptionsAIO,
)
from mlex_utils.dash_utils.components_mantime.component_utils import (
    DmcControlItem,
    _tooltip,
)


class DmcJobManagerMinimalAIO(html.Div):

    class ids:

        job_name_title = lambda aio_id: {  # noqa: E731
            "component": "DmcJobManagerAIO",
            "subcomponent": "job-name-title",
            "aio_id": aio_id,
        }

        job_name = lambda aio_id: {  # noqa: E731
            "component": "DmcJobManagerAIO",
            "subcomponent": "job-name",
            "aio_id": aio_id,
        }

        run_button = lambda aio_id: {  # noqa: E731
            "component": "DmcJobManagerAIO",
            "subcomponent": "run-button",
            "aio_id": aio_id,
        }

        run_dropdown_title = lambda aio_id: {  # noqa: E731
            "component": "DmcJobManagerAIO",
            "subcomponent": "run-dropdown-title",
            "aio_id": aio_id,
        }

        run_dropdown = lambda aio_id: {  # noqa: E731
            "component": "DmcJobManagerAIO",
            "subcomponent": "run-dropdown",
            "aio_id": aio_id,
        }

        advanced_options_modal_run = lambda aio_id: {  # noqa: E731
            "component": "DmcJobManagerAIO",
            "subcomponent": "advanced-options-modal-run",
            "aio_id": aio_id,
        }

        advanced_options_modal = lambda aio_id: {  # noqa: E731
            "component": "DmcJobManagerAIO",
            "subcomponent": "advanced-options-modal",
            "aio_id": aio_id,
        }

        check_job = lambda aio_id: {  # noqa: E731
            "component": "DmcJobManagerAIO",
            "subcomponent": "check-job",
            "aio_id": aio_id,
        }

        project_name_id = lambda aio_id: {  # noqa: E731
            "component": "DmcJobManagerAIO",
            "subcomponent": "project-name-id",
            "aio_id": aio_id,
        }

        notifications_container = lambda aio_id: {  # noqa: E731
            "component": "DmcJobManagerAIO",
            "subcomponent": "notifications-container",
            "aio_id": aio_id,
        }

        model_parameters = lambda aio_id: {  # noqa: E731
            "component": "DmcJobManagerAIO",
            "subcomponent": "model-parameters",
            "aio_id": aio_id,
        }

        model_list_title = lambda aio_id: {  # noqa: E731
            "component": "DmcJobManagerAIO",
            "subcomponent": "model-list-title",
            "aio_id": aio_id,
        }

        model_list = lambda aio_id: {  # noqa: E731
            "component": "DmcJobManagerAIO",
            "subcomponent": "model-list",
            "aio_id": aio_id,
        }

    ids = ids

    def __init__(
        self,
        model_list=["Test Model"],
        prefect_tags=[],
        mode="dev",
        run_button_props=None,
        modal_props=None,
        aio_id=None,
        dependency=None,
    ):
        """
        DmcJobManagerAIO is an All-in-One component that is composed
        of a parent `html.Div` with a button to run and infer a model.
        - `model_list` - A list of models
        - `prefect_tags` - A list of tags used to filter Prefect flow runs.
        - `mode` - The mode of the component. If "dev", the component will display sample data.
        - `run_button_props` - A dictionary of properties passed into the Button component for the run button.
        - `modal_props` - A dictionary of properties passed into the Modal component for the advanced options modal.
        - `aio_id` - The All-in-One component ID used to generate the markdown and dropdown components's dictionary IDs.
        - `dependency` - List of jobs is dependent on the completion of the value of this component (dropdown).
        """
        if aio_id is None:
            aio_id = str(uuid.uuid4())

        if run_button_props is None:
            run_button_props = {
                "variant": "light",
                "style": {"width": "100%", "margin": "5px"},
            }

        if modal_props is None:
            modal_props = {"style": {"margin": "10px 10px 10px 250px"}}

        self._aio_id = aio_id
        self._prefect_tags = prefect_tags
        self._mode = mode
        self._dependency = dependency

        super().__init__(
            [
                DmcControlItem(
                    "Algorithm",
                    self.ids.model_list_title(aio_id),
                    dmc.Select(
                        id=self.ids.model_list(aio_id),
                        data=model_list,
                        value=(model_list[0] if model_list[0] else None),
                    ),
                ),
                dmc.Space(h=15),
                html.Div(id=self.ids.model_parameters(aio_id)),
                dmc.Space(h=25),
                DmcControlItem(
                    "Name",
                    self.ids.job_name_title(aio_id),
                    dmc.TextInput(
                        placeholder="Name your job...",
                        id=self.ids.job_name(aio_id),
                    ),
                ),
                dmc.Space(h=10),
                dmc.Button("Run", id=self.ids.run_button(aio_id), **run_button_props),
                dmc.Space(h=10),
                DmcControlItem(
                    "Jobs",
                    self.ids.run_dropdown_title(aio_id),
                    dmc.Grid(
                        [
                            dmc.Select(
                                placeholder="Select a job...",
                                id=self.ids.run_dropdown(aio_id),
                            ),
                            dmc.ActionIcon(
                                _tooltip(
                                    "Advanced Options",
                                    children=[
                                        DashIconify(
                                            icon="mdi:settings-applications",
                                            width=30,
                                        ),
                                    ],
                                ),
                                size="xs",
                                variant="subtle",
                                id=self.ids.advanced_options_modal_run(aio_id),
                                n_clicks=0,
                                style={"margin": "auto"},
                            ),
                        ],
                        style={"margin": "0px"},
                    ),
                ),
                dmc.Space(h=25),
                DmcAdvancedOptionsAIO(aio_id=aio_id),
                html.Div(id=self.ids.notifications_container(aio_id)),
                dcc.Interval(
                    id=self.ids.check_job(aio_id),
                    interval=5000,
                ),
                dcc.Store(
                    id=self.ids.project_name_id(aio_id),
                    data="",
                ),
            ]
        )

        self.register_callbacks()

    @staticmethod
    @callback(
        Output(
            {
                "aio_id": MATCH,
                "component": "DmcAdvancedOptionsAIO",
                "subcomponent": "advanced-options-modal",
            },
            "opened",
        ),
        Output(
            {
                "aio_id": MATCH,
                "component": "DmcAdvancedOptionsAIO",
                "subcomponent": "job-id",
            },
            "data",
        ),
        Input(ids.advanced_options_modal_run(MATCH), "n_clicks"),
        State(
            {
                "aio_id": MATCH,
                "component": "DmcAdvancedOptionsAIO",
                "subcomponent": "advanced-options-modal",
            },
            "opened",
        ),
        State(ids.run_dropdown(MATCH), "value"),
        prevent_initial_call=True,
    )
    def toggle_modal(n1, is_open, run_job_id):
        return not is_open, run_job_id

    @staticmethod
    @callback(
        Output(ids.advanced_options_modal_run(MATCH), "disabled"),
        Input(ids.run_dropdown(MATCH), "value"),
    )
    def disable_advanced_run_options(run_job_id):
        if run_job_id is not None:
            return False
        return True

    def register_callbacks(self):

        @callback(
            Output(self.ids.run_dropdown(self._aio_id), "data"),
            Input(self.ids.check_job(self._aio_id), "n_intervals"),
        )
        def check_run_job(n_intervals):
            return _check_train_job(self._prefect_tags, self._mode)

        @callback(
            Output(
                {
                    "aio_id": self._aio_id,
                    "component": "DmcAdvancedOptionsAIO",
                    "subcomponent": "advanced-options-modal",
                },
                "opened",
                allow_duplicate=True,
            ),
            Input(
                {
                    "aio_id": self._aio_id,
                    "component": "DmcAdvancedOptionsAIO",
                    "subcomponent": "warning-confirm-cancel",
                },
                "n_clicks",
            ),
            State(
                {
                    "aio_id": self._aio_id,
                    "component": "DmcAdvancedOptionsAIO",
                    "subcomponent": "job-id",
                },
                "data",
            ),
            prevent_initial_call=True,
        )
        def cancel_job(n_clicks, job_id):
            _cancel_job(job_id, self._mode)
            return False

        @callback(
            Output(self.ids.run_dropdown(self._aio_id), "value", allow_duplicate=True),
            Output(
                {
                    "aio_id": self._aio_id,
                    "component": "DmcAdvancedOptionsAIO",
                    "subcomponent": "advanced-options-modal",
                },
                "opened",
                allow_duplicate=True,
            ),
            Input(
                {
                    "aio_id": self._aio_id,
                    "component": "DmcAdvancedOptionsAIO",
                    "subcomponent": "warning-confirm-delete",
                },
                "n_clicks",
            ),
            State(
                {
                    "aio_id": self._aio_id,
                    "component": "DmcAdvancedOptionsAIO",
                    "subcomponent": "job-id",
                },
                "data",
            ),
            State(self.ids.run_dropdown(self._aio_id), "value"),
            prevent_initial_call=True,
        )
        def delete_job(n_clicks, job_id, run_job_id):
            _delete_job(job_id, self._mode)
            return None, False

        @callback(
            Output(
                {
                    "aio_id": self._aio_id,
                    "component": "DmcAdvancedOptionsAIO",
                    "subcomponent": "logs-area",
                },
                "children",
            ),
            Input(
                {
                    "aio_id": self._aio_id,
                    "component": "DmcAdvancedOptionsAIO",
                    "subcomponent": "advanced-options-modal",
                },
                "opened",
            ),
            Input(self.ids.check_job(self._aio_id), "n_intervals"),
            State(
                {
                    "aio_id": self._aio_id,
                    "component": "DmcAdvancedOptionsAIO",
                    "subcomponent": "job-id",
                },
                "data",
            ),
            prevent_initial_call=True,
        )
        def get_logs(is_open, n_intervals, job_id):
            if job_id is None:
                return "No logs available"
            return _get_job_logs(job_id, self._mode)

        if self._dependency:

            @callback(
                Output(
                    self.ids.run_dropdown(self._aio_id), "data", allow_duplicate=True
                ),
                Output(self.ids.run_dropdown(self._aio_id), "value"),
                Input(self.ids.check_job(self._aio_id), "n_intervals"),
                Input(self._dependency, "value"),
                State(self.ids.project_name_id(self._aio_id), "data"),
                prevent_initial_call=True,
            )
            def check_dependant_job(n_intervals, dependant_job_id, project_name):
                return _check_inference_job(
                    dependant_job_id, project_name, self._prefect_tags, self._mode
                )
