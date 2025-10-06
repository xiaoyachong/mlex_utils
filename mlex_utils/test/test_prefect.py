import asyncio
import uuid

from prefect import context, flow, get_client
from prefect.client.schemas.objects import StateType
from prefect.testing.utilities import prefect_test_harness

from mlex_utils.prefect_utils.core import (
    cancel_flow_run,
    delete_flow_run,
    get_children_flow_run_ids,
    get_flow_run_logs,
    get_flow_run_name,
    get_flow_run_parameters,
    get_flow_run_state,
    query_flow_runs,
    schedule_prefect_flow,
)


@flow(name="Child Flow 1")
def child_flow1():
    return "Success1"


@flow(name="Child Flow 2")
def child_flow2():
    return "Success2"


@flow(name="Parent Flow")
def parent_flow(model_name):
    parent_flow_run_id = context.get_run_context().flow_run.id
    child_flow1()
    child_flow2()
    return parent_flow_run_id


def run_flow():
    """
    Run the parent flow inline (no workers/agents) and return the flow run ID.
    """
    flow_run_id = parent_flow(model_name="model_name")
    print(f"Parent flow finished with run ID: {flow_run_id}")
    return flow_run_id


def test_schedule_prefect_flows():
    with prefect_test_harness():
        deployment = parent_flow.to_deployment(
            name="test_deployment", tags=["Test tag"], version="1"
        )
        # Add deployment
        deployment.apply()

        # Schedule parent flow
        flow_run_id = schedule_prefect_flow(
            deployment_name="Parent Flow/test_deployment",
            parameters={"model_name": "model_name"},
            flow_run_name="flow_run_name",
        )

        print(f"Successfully scheduled flow run with ID: {flow_run_id}")
        assert isinstance(flow_run_id, uuid.UUID)


def test_monitor_prefect_flow_runs():
    with prefect_test_harness():
        # Run flow
        flow_run_id = run_flow()
        assert isinstance(flow_run_id, uuid.UUID)

        # Get flow runs by name
        flow_runs = query_flow_runs()
        assert len(flow_runs) == 3

        # Get flow run name
        flow_run_name = get_flow_run_name(flow_run_id)
        assert isinstance(flow_run_name, str)

        # Get children flow run ids
        children_flow_run_ids = get_children_flow_run_ids(flow_run_id)
        assert len(children_flow_run_ids) == 2


def test_delete_prefect_flow_runs():
    with prefect_test_harness():
        # Run flow
        flow_run_id = run_flow()
        assert isinstance(flow_run_id, uuid.UUID)

        # Get flow runs by name
        flow_runs = query_flow_runs()
        assert len(flow_runs) == 3

        # Delete flow run
        delete_flow_run(flow_run_id)

        # Get flow runs by name
        flow_runs = query_flow_runs()
        assert len(flow_runs) < 3


def test_cancel_prefect_flow_runs():
    with prefect_test_harness():
        deployment = parent_flow.to_deployment(
            name="test_deployment",
            version="1",
            tags=["Test tag"],
        )
        # Add deployment
        deployment.apply()

        # Schedule parent flow
        flow_run_id = schedule_prefect_flow(
            deployment_name="Parent Flow/test_deployment",
            parameters={"model_name": "model_name"},
            flow_run_name="flow_run_name",
        )

        # Change flow run state
        flow_run_state = get_flow_run_state(flow_run_id)
        assert flow_run_state not in [StateType.COMPLETED, StateType.FAILED]

        # Cancel flow run
        cancel_flow_run(flow_run_id)

        # Check status in name
        flow_run_name = get_flow_run_name(flow_run_id)
        flow_run_label = query_flow_runs(flow_run_name)[0]["label"]
        assert flow_run_label[0] == "🚫"


def test_get_flow_run_logs():
    with prefect_test_harness():
        # Run flow
        flow_run_id = run_flow()
        assert isinstance(flow_run_id, uuid.UUID)

        # Get flow run logs
        flow_run_logs = get_flow_run_logs(flow_run_id)
        print(f"Parent flow finished with flow_run_logs: {flow_run_logs}")
        assert isinstance(flow_run_logs, list)


def test_get_flow_run_parameters():
    with prefect_test_harness():
        # Run flow
        flow_run_id = run_flow()
        assert isinstance(flow_run_id, uuid.UUID)

        # Get flow run logs
        flow_run_parameters = get_flow_run_parameters(flow_run_id)
        assert isinstance(flow_run_parameters, dict)
