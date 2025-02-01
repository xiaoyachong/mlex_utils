import uuid
from contextvars import copy_context

import pytest
from dash._callback_context import context_value
from dash._utils import AttributeDict

from mlex_utils.dash_utils.components_bootstrap.advanced_options import (
    DbcAdvancedOptionsAIO,
)
from mlex_utils.dash_utils.components_mantime.advanced_options import (
    DmcAdvancedOptionsAIO,
)
from mlex_utils.dash_utils.mlex_components import MLExComponents

model_parameters = [
    {
        "type": "float",
        "name": "float_param",
        "title": "Float Parameter",
        "param_key": "float_param",
        "value": 1,
        "comp_group": "group_1",
    },
    {
        "type": "int",
        "name": "int_param",
        "title": "Integer Parameter",
        "param_key": "int_param",
        "value": 1,
        "comp_group": "group_1",
    },
    {
        "type": "str",
        "name": "str_param",
        "title": "String Parameter",
        "param_key": "str_param",
        "value": "test",
        "comp_group": "group_1",
    },
    {
        "type": "slider",
        "name": "slider",
        "title": "Slider",
        "param_key": "slider",
        "min": 1,
        "max": 1000,
        "value": 30,
        "comp_group": "group_1",
    },
    {
        "type": "dropdown",
        "name": "dropdown",
        "title": "Dropdown",
        "param_key": "dropdown",
        "comp_group": "group_1",
    },
    {
        "type": "radio",
        "name": "radio",
        "title": "Radio",
        "param_key": "radio",
        "options": [
            {"label": "Option 1", "value": 1},
            {"label": "Option 2", "value": 2},
        ],
        "comp_group": "group_1",
    },
    {
        "type": "bool",
        "name": "bool",
        "title": "Bool",
        "param_key": "bool",
        "comp_group": "group_1",
    },
]

new_values = {
    "float_param": 2.0,
    "int_param": 2,
    "str_param": "test2",
    "slider": 50,
    "dropdown": "option_1",
    "radio": 2,
    "bool": True,
}


def serialize_dash_components(obj):
    if hasattr(obj, "to_plotly_json"):
        # Serialize the Dash component
        serialized_obj = obj.to_plotly_json()
        # Recursively process the serialized object's props
        if isinstance(serialized_obj, dict) and "props" in serialized_obj:
            serialized_obj["props"] = serialize_dash_components(serialized_obj["props"])
        return serialized_obj
    elif isinstance(obj, dict):
        # Recursively process dictionary items
        return {key: serialize_dash_components(value) for key, value in obj.items()}
    elif isinstance(obj, (list, tuple)):
        # Recursively process list or tuple items
        return [serialize_dash_components(item) for item in obj]
    else:
        # Return the object as is (e.g., strings, numbers)
        return obj


@pytest.mark.parametrize("component_type", ["dbc", "dmc"])
def test_get_job_manager(component_type):
    mlex_components = MLExComponents(component_type)
    job_manager = mlex_components.get_job_manager()
    assert job_manager is not None


@pytest.mark.parametrize("component_type", ["dbc", "dmc"])
def test_get_job_manager_minimal(component_type):
    mlex_components = MLExComponents(component_type)
    job_manager = mlex_components.get_job_manager_minimal()
    assert job_manager is not None


@pytest.mark.parametrize("component_type", ["dbc", "dmc"])
def test_advanced_options_modal(component_type):
    mlex_components = MLExComponents(component_type)
    job_manager = mlex_components.get_job_manager()

    def run_callback(n1, n2, is_open, train_job_id, inference_job_id, prop_id):
        context_value.set(AttributeDict(**{"triggered_inputs": [{"prop_id": prop_id}]}))
        return job_manager.toggle_modal(n1, n2, is_open, train_job_id, inference_job_id)

    ctx = copy_context()

    # Open advanced options modal with train job id
    output = ctx.run(
        run_callback, 1, 0, False, "uid0001", None, "train-button.n_clicks"
    )
    assert output[0] is True and output[1] == "uid0001"

    # Close advanced options modal
    output = ctx.run(run_callback, 0, 1, True, None, None, "train-button.n_clicks")
    assert output[0] is False and output[1] is None

    # Open advanced options modal with no inference job id
    output = ctx.run(run_callback, 0, 1, False, None, None, "inference-button.n_clicks")
    assert output[0] is True and output[1] is None

    # Disable train advanced options modal button
    assert not job_manager.disable_advanced_train_options("uid0001")

    # Disable inference advanced options modal button
    assert job_manager.disable_advanced_inference_options(None)


@pytest.mark.parametrize("component_type", ["dbc", "dmc"])
def test_get_parameters(component_type):
    mlex_components = MLExComponents(component_type)
    parameters = mlex_components.get_parameter_items(
        _id={"type": str(uuid.uuid4())}, json_blob=model_parameters
    )
    assert parameters is not None
    parameters = serialize_dash_components(parameters)
    parameters_dict, params_errors = mlex_components.get_parameters_values(parameters)
    assert isinstance(parameters_dict, dict) and params_errors is False


@pytest.mark.parametrize("component_type", ["dbc", "dmc"])
def test_get_and_update_parameters(component_type):
    mlex_components = MLExComponents(component_type)
    parameters = mlex_components.get_parameter_items(
        _id={"type": str(uuid.uuid4())}, json_blob=model_parameters
    )
    assert parameters is not None
    parameters = serialize_dash_components(parameters)
    parameters_dict, params_errors = mlex_components.get_parameters_values(parameters)
    assert isinstance(parameters_dict, dict) and params_errors is False

    new_parameters = mlex_components.update_parameters_values(parameters, new_values)
    assert new_parameters is not None
    new_parameters = serialize_dash_components(new_parameters)
    new_parameters_dict, new_params_errors = mlex_components.get_parameters_values(
        new_parameters
    )
    assert isinstance(new_parameters_dict, dict) and new_params_errors is False


def test_toggle_warnings_dbc():
    assert not DbcAdvancedOptionsAIO.toggle_warning_cancel_modal(0, 0, True)
    assert DbcAdvancedOptionsAIO.toggle_warning_delete_modal(0, 0, False)


def test_toggle_warnings_dmc():
    assert not DmcAdvancedOptionsAIO.toggle_warning_cancel_modal(0, 0, 0, True)
    assert DmcAdvancedOptionsAIO.toggle_warning_delete_modal(0, 0, 1, False)
