from dash import html, no_update

from mlex_utils.prefect_utils.core import (
    cancel_flow_run,
    delete_flow_run,
    get_flow_run_logs,
    get_flow_run_name,
    get_flow_run_state,
    query_flow_runs,
)

DEV_JOBS = [
    {"label": "❌ DLSIA ABC 03/11/2024 15:38PM", "value": "uid0001"},
    {"label": "🕑 DLSIA XYC 03/11/2024 14:21PM", "value": "uid0002"},
    {"label": "✅ DLSIA CBA 03/11/2024 10:02AM", "value": "uid0003"},
]


def _check_job(prefect_tags, mode):
    if mode == "dev":
        data = DEV_JOBS
    else:
        data = query_flow_runs(tags=prefect_tags)
    return data


def _check_train_job(prefect_tags, mode):
    """
    This callback populates the train job selector dropdown with job names and ids from Prefect.
    The list of jobs is filtered by the selected project in the project selector dropdown.
    This callback displays the current status of the job as part of the job name in the dropdown.
    In "dev" mode, the dropdown is populated with the sample data above.
    """
    return _check_job(prefect_tags + ["train"], mode)


def _check_dependent_job(job_id, project_name, prefect_tags, mode):
    if mode == "dev":
        return DEV_JOBS, no_update
    else:
        if job_id is not None and get_flow_run_state(job_id) == "COMPLETED":
            job_name = get_flow_run_name(job_id)
            if job_name is not None:
                data = query_flow_runs(
                    flow_run_name=job_name,
                    tags=prefect_tags.append(project_name),
                )
                selected_value = None if len(data) == 0 else no_update
            return data, selected_value
        return [], None


def _check_inference_job(train_job_id, project_name, prefect_tags, mode):
    """
    This callback populates the inference job selector dropdown with job names and ids from Prefect.
    The list of jobs is filtered by the selected train job in the train job selector dropdown.
    The selected value is set to None if the list of jobs is empty.
    This callback displays the current status of the job as part of the job name in the dropdown.
    In "dev" mode, the dropdown is populated with the sample data above.
    """
    return _check_dependent_job(
        train_job_id, project_name, prefect_tags + ["inference"], mode
    )


def _get_job_logs(job_id, mode):
    """
    This callback retrieves the logs of the selected job from Prefect.
    The logs are displayed in the logs textarea.
    In "dev" mode, the logs are retrieved from the sample data above.
    """
    if mode == "dev":
        return "Sample logs"
    else:
        logs = get_flow_run_logs(job_id)
        return [item for pair in zip(logs, [html.Br()] * len(logs)) for item in pair][
            :-1
        ]


def _cancel_job(job_id, mode):
    """
    This callback cancels the selected job in Prefect.
    """
    if mode != "dev":
        cancel_flow_run(job_id)
    pass


def _delete_job(job_id, mode):
    """
    This callback deletes the selected job in Prefect.
    """
    if mode != "dev":
        delete_flow_run(job_id)
    pass
