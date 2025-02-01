import uuid

import dash_bootstrap_components as dbc
from dash import MATCH, Input, Output, State, callback, dcc, html
from dash_iconify import DashIconify

from mlex_utils.dash_utils.callbacks.manage_jobs import (
    _cancel_job,
    _check_dependent_job,
    _check_job,
    _delete_job,
    _get_job_logs,
)
from mlex_utils.dash_utils.components_bootstrap.advanced_options import (
    DbcAdvancedOptionsAIO,
)
from mlex_utils.dash_utils.components_bootstrap.component_utils import DbcControlItem


class DbcJobManagerMinimalAIO(html.Div):

    class ids:

        job_name_title = lambda aio_id: {  # noqa: E731
            "component": "DbcJobManagerAIO",
            "subcomponent": "job-name-title",
            "aio_id": aio_id,
        }

        job_name = lambda aio_id: {  # noqa: E731
            "component": "DbcJobManagerAIO",
            "subcomponent": "job-name",
            "aio_id": aio_id,
        }

        run_button = lambda aio_id: {  # noqa: E731
            "component": "DbcJobManagerAIO",
            "subcomponent": "run-button",
            "aio_id": aio_id,
        }

        run_dropdown_title = lambda aio_id: {  # noqa: E731
            "component": "DbcJobManagerAIO",
            "subcomponent": "run-dropdown-title",
            "aio_id": aio_id,
        }

        run_dropdown = lambda aio_id: {  # noqa: E731
            "component": "DbcJobManagerAIO",
            "subcomponent": "run-dropdown",
            "aio_id": aio_id,
        }

        advanced_options_modal_run = lambda aio_id: {  # noqa: E731
            "component": "DbcJobManagerAIO",
            "subcomponent": "advanced-options-modal-run",
            "aio_id": aio_id,
        }

        check_job = lambda aio_id: {  # noqa: E731
            "component": "DbcJobManagerAIO",
            "subcomponent": "check-job",
            "aio_id": aio_id,
        }

        project_name_id = lambda aio_id: {  # noqa: E731
            "component": "DbcJobManagerAIO",
            "subcomponent": "project-name-id",
            "aio_id": aio_id,
        }

        notifications_container = lambda aio_id: {  # noqa: E731
            "component": "DbcJobManagerAIO",
            "subcomponent": "notifications-container",
            "aio_id": aio_id,
        }

        model_parameters = lambda aio_id: {  # noqa: E731
            "component": "DbcJobManagerAIO",
            "subcomponent": "model-parameters",
            "aio_id": aio_id,
        }

        model_list_title = lambda aio_id: {  # noqa: E731
            "component": "DbcJobManagerAIO",
            "subcomponent": "model-list-title",
            "aio_id": aio_id,
        }

        model_list = lambda aio_id: {  # noqa: E731
            "component": "DbcJobManagerAIO",
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
        dependency_id=None,
    ):
        """
        DbcJobManagerAIO is an All-in-One component that is composed
        of a parent `html.Div` with a button to run and infer a model.
        - `model_list` - A list of models
        - `prefect_tags` - A list of tags used to filter Prefect flow runs.
        - `mode` - The mode of the component. If "dev", the component will display sample data.
        - `run_button_props` - A dictionary of properties passed into the Button component for the run button.
        - `modal_props` - A dictionary of properties passed into the Modal component for the advanced options modal.
        - `aio_id` - The All-in-One component ID used to generate the markdown and dropdown components's dictionary IDs.
        - `dependency_id` - Check list of jobs that are dependent on the completion of the job of this component id
                            (dropdown).
        """
        if aio_id is None:
            aio_id = str(uuid.uuid4())

        if run_button_props is None:
            run_button_props = {"color": "primary", "style": {"width": "100%"}}
        if modal_props is None:
            modal_props = {"style": {}}

        self._aio_id = aio_id
        self._prefect_tags = prefect_tags
        self._mode = mode
        self._dependency_id = dependency_id

        super().__init__(
            [
                DbcControlItem(
                    "Algorithm",
                    self.ids.model_list_title(aio_id),
                    dbc.Select(
                        id=self.ids.model_list(aio_id),
                        options=[
                            {"label": model, "value": model} for model in model_list
                        ],
                        value=(model_list[0] if model_list[0] else None),
                    ),
                ),
                html.Div(id=self.ids.model_parameters(aio_id)),
                html.P(),
                DbcControlItem(
                    "Name",
                    self.ids.job_name_title(aio_id),
                    dbc.Input(
                        id=self.ids.job_name(aio_id),
                        type="text",
                        placeholder="Name your job...",
                        style={"width": "100%"},
                    ),
                ),
                html.Div(style={"height": "10px"}),
                dbc.Button("Run", id=self.ids.run_button(aio_id), **run_button_props),
                html.Div(style={"height": "10px"}),
                DbcControlItem(
                    "Jobs",
                    self.ids.run_dropdown_title(aio_id),
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Select(
                                        id=self.ids.run_dropdown(aio_id),
                                    ),
                                    width=10,
                                ),
                                dbc.Col(
                                    dbc.Button(
                                        DashIconify(
                                            icon="mdi:settings",
                                            style={"padding": "0px"},
                                        ),
                                        id=self.ids.advanced_options_modal_run(aio_id),
                                        color="secondary",
                                        style={"height": "36px", "line-height": "1"},
                                    ),
                                    width=2,
                                ),
                            ],
                            className="g-1",
                        ),
                    ],
                ),
                html.Div(style={"height": "10px"}),
                DbcAdvancedOptionsAIO(aio_id=aio_id),
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
                "component": "DbcAdvancedOptionsAIO",
                "subcomponent": "advanced-options-modal",
            },
            "is_open",
        ),
        Output(
            {
                "aio_id": MATCH,
                "component": "DbcAdvancedOptionsAIO",
                "subcomponent": "job-id",
            },
            "data",
        ),
        Input(ids.advanced_options_modal_run(MATCH), "n_clicks"),
        State(
            {
                "aio_id": MATCH,
                "component": "DbcAdvancedOptionsAIO",
                "subcomponent": "advanced-options-modal",
            },
            "is_open",
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
            Output(
                {
                    "aio_id": self._aio_id,
                    "component": "DbcAdvancedOptionsAIO",
                    "subcomponent": "advanced-options-modal",
                },
                "is_open",
                allow_duplicate=True,
            ),
            Input(
                {
                    "aio_id": self._aio_id,
                    "component": "DbcAdvancedOptionsAIO",
                    "subcomponent": "warning-confirm-cancel",
                },
                "n_clicks",
            ),
            State(
                {
                    "aio_id": self._aio_id,
                    "component": "DbcAdvancedOptionsAIO",
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
                    "component": "DbcAdvancedOptionsAIO",
                    "subcomponent": "advanced-options-modal",
                },
                "is_open",
                allow_duplicate=True,
            ),
            Input(
                {
                    "aio_id": self._aio_id,
                    "component": "DbcAdvancedOptionsAIO",
                    "subcomponent": "warning-confirm-delete",
                },
                "n_clicks",
            ),
            State(
                {
                    "aio_id": self._aio_id,
                    "component": "DbcAdvancedOptionsAIO",
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
                    "component": "DbcAdvancedOptionsAIO",
                    "subcomponent": "logs-area",
                },
                "children",
            ),
            Input(
                {
                    "aio_id": self._aio_id,
                    "component": "DbcAdvancedOptionsAIO",
                    "subcomponent": "advanced-options-modal",
                },
                "is_open",
            ),
            Input(self.ids.check_job(self._aio_id), "n_intervals"),
            State(
                {
                    "aio_id": self._aio_id,
                    "component": "DbcAdvancedOptionsAIO",
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

        if self._dependency_id is not None:

            @callback(
                Output(
                    self.ids.run_dropdown(self._aio_id), "options", allow_duplicate=True
                ),
                Output(self.ids.run_dropdown(self._aio_id), "value"),
                Input(self.ids.check_job(self._aio_id), "n_intervals"),
                Input(self._dependency_id, "value"),
                State(self.ids.project_name_id(self._aio_id), "data"),
                prevent_initial_call=True,
            )
            def check_dependent_job(n_intervals, dependent_job_id, project_name):
                jobs = _check_dependent_job(
                    dependent_job_id, project_name, self._prefect_tags, self._mode
                )
                return jobs

        else:

            @callback(
                Output(self.ids.run_dropdown(self._aio_id), "options"),
                Input(self.ids.check_job(self._aio_id), "n_intervals"),
            )
            def check_run_job(n_intervals):
                return _check_job(self._prefect_tags, self._mode)
