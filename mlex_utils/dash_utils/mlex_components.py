import importlib

UI_STYLE_IMPLEMENTATIONS = {
    "dbc": {
        "job_manager": "mlex_utils.dash_utils.components_bootstrap.job_manager.DbcJobManagerAIO",
        "job_manager_minimal": (
            "mlex_utils.dash_utils.components_bootstrap."
            "job_manager_minimal.DbcJobManagerMinimalAIO"
        ),
        "parameter_items": (
            "mlex_utils.dash_utils.components_bootstrap.parameter_items."
            "DbcParameterItems"
        ),
    },
    "dmc": {
        "job_manager": "mlex_utils.dash_utils.components_mantime.job_manager.DmcJobManagerAIO",
        "job_manager_minimal": (
            "mlex_utils.dash_utils.components_mantime."
            "job_manager_minimal.DmcJobManagerMinimalAIO"
        ),
        "parameter_items": (
            "mlex_utils.dash_utils.components_mantime.parameter_items."
            "DmcParameterItems"
        ),
    },
}


def import_from_path(import_path: str):
    """Dynamically import a class/function given its full import path."""
    module_path, attr_name = import_path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    return getattr(module, attr_name)


class MLExComponents:
    ALLOWED_UI_STYLES = {"dbc", "dmc"}

    def __init__(self, ui_style):
        if ui_style not in self.ALLOWED_UI_STYLES:
            raise ValueError(
                f"ui_style must be one of {self.ALLOWED_UI_STYLES}, got {ui_style}"
            )
        self.ui_style = ui_style

    def get_job_manager(self, **kwargs):
        path = UI_STYLE_IMPLEMENTATIONS[self.ui_style]["job_manager"]
        cls = import_from_path(path)
        return cls(**kwargs)

    def get_job_manager_minimal(self, **kwargs):
        path = UI_STYLE_IMPLEMENTATIONS[self.ui_style]["job_manager_minimal"]
        cls = import_from_path(path)
        return cls(**kwargs)

    def get_parameter_items(self, **kwargs):
        path = UI_STYLE_IMPLEMENTATIONS[self.ui_style]["parameter_items"]
        cls = import_from_path(path)
        return cls(**kwargs)

    @staticmethod
    def get_parameters_values(parameters):
        """
        Extracts parameters from the children component of a ParameterItems component,
        if there are any errors in the input, it will return an error status
        """
        errors = False
        input_params = {}
        for param in parameters["props"]["children"]:
            # param["props"]["children"][0] is the label
            # param["props"]["children"][1] is the input
            parameter_container = param["props"]["children"][1]
            # The actual parameter item is the first and only child of the parameter container
            parameter_item = parameter_container["props"]["children"]["props"]
            key = parameter_item["id"]["param_key"]
            if "value" in parameter_item:
                value = parameter_item["value"]
            elif "checked" in parameter_item:
                value = parameter_item["checked"]
            if "error" in parameter_item:
                if parameter_item["error"] is not False:
                    errors = True
            input_params[key] = value
        return input_params, errors

    # TODO: Consider changing the background of the components to indicate the change
    @staticmethod
    def update_parameters_values(current_parameters, new_values):
        """
        Updates the current parameters with the new values
        """
        parameters_children = current_parameters["props"].get("children", [])

        for param in parameters_children:
            # param["props"]["children"][1] is the container for the input
            # The actual input props are at ["props"]["children"]["props"]
            input_props = param["props"]["children"][1]["props"]["children"]["props"]
            key = input_props["id"]["param_key"]

            if key in new_values:
                value = new_values[key]
                # Update "value" if present, otherwise "checked"
                if "value" in input_props:
                    input_props["value"] = value
                elif "checked" in input_props:
                    input_props["checked"] = bool(value)

        return current_parameters
