import asyncio
import uuid

from prefect import context, flow, get_client
from prefect.client.schemas.objects import StateType
from prefect.deployments import Deployment
from prefect.engine import create_then_begin_flow_run
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


# Note: The name of the flow should avoid the use of "_" in this version of Prefect
# https://github.com/PrefectHQ/prefect/pull/7920
# TODO: Consider upgrading to a newer version of Prefect
@flow(name="Child Flow 1")
def child_flow1():
    return "Success1"


@flow(name="Child Flow 2")
def child_flow2():
    return "Success2"


@flow(name="Parent Flow")
def parent_flow(model_name):
    parent_flow_run_id = str(context.get_run_context().flow_run.id)
    child_flow1()
    child_flow2()
    return parent_flow_run_id


async def run_flow():
    async with get_client() as client:
        flow_run_id = await create_then_begin_flow_run(
            parent_flow,
            parameters={"model_name": "model_name"},
            return_type="result",
            client=client,
            wait_for=True,
            user_thread=False,
        )
    return flow_run_id


def test_schedule_prefect_flows():
    with prefect_test_harness():
        deployment = Deployment.build_from_flow(
            flow=parent_flow,
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
        assert isinstance(flow_run_id, uuid.UUID)


def test_monitor_prefect_flow_runs():
    with prefect_test_harness():
        # Run flow
        flow_run_id = asyncio.run(run_flow())
        assert isinstance(flow_run_id, str)

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
        flow_run_id = asyncio.run(run_flow())
        assert isinstance(flow_run_id, str)

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
        deployment = Deployment.build_from_flow(
            flow=parent_flow,
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
        flow_run_id = asyncio.run(run_flow())
        assert isinstance(flow_run_id, str)

        # Get flow run logs
        flow_run_logs = get_flow_run_logs(flow_run_id)
        assert len(flow_run_logs) > 0
        assert isinstance(flow_run_logs[0], str)


def test_get_flow_run_parameters():
    with prefect_test_harness():
        # Run flow
        flow_run_id = asyncio.run(run_flow())
        assert isinstance(flow_run_id, str)

        # Get flow run logs
        flow_run_parameters = get_flow_run_parameters(flow_run_id)
        assert isinstance(flow_run_parameters, dict)
