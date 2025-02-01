import dash_bootstrap_components as dbc
from dash import dcc

from mlex_utils.dash_utils.components_bootstrap.component_utils import DbcControlItem


class DbcSimpleItem(DbcControlItem):
    def __init__(
        self,
        name,
        base_id,
        item_type,
        title=None,
        param_key=None,
        visible=True,
        debounce=True,
        **kwargs,
    ):

        if param_key is None:
            param_key = name

        self.input = dbc.Input(
            type=item_type,
            debounce=debounce,
            id={**base_id, "name": name, "param_key": param_key, "layer": "input"},
            **kwargs,
        )

        style = {"padding": "15px 0px 0px 0px"}
        if not visible:
            style["display"] = "none"

        super(DbcSimpleItem, self).__init__(
            title=title,
            title_id={
                **base_id,
                "name": name,
                "param_key": param_key,
                "layer": "label",
            },
            item=self.input,
            style=style,
        )


class DbcNumberItem(DbcSimpleItem):
    def __init__(self, *args, **kwargs):
        super(DbcNumberItem, self).__init__(*args, item_type="number", **kwargs)


class DbcStrItem(DbcSimpleItem):
    def __init__(self, *args, **kwargs):
        super(DbcStrItem, self).__init__(*args, item_type="text", **kwargs)


class DbcSliderItem(DbcControlItem):
    def __init__(
        self, name, base_id, title=None, param_key=None, visible=True, **kwargs
    ):

        if param_key is None:
            param_key = name

        self.input = dcc.Slider(
            id={**base_id, "name": name, "param_key": param_key, "layer": "input"},
            tooltip={"placement": "bottom", "always_visible": True},
            **kwargs,
        )

        style = {"padding": "15px 0px 0px 0px"}
        if not visible:
            style["display"] = "none"

        super(DbcSliderItem, self).__init__(
            title=title,
            title_id={
                **base_id,
                "name": name,
                "param_key": param_key,
                "layer": "label",
            },
            item=self.input,
            style=style,
        )


class DbcDropdownItem(DbcControlItem):
    def __init__(
        self, name, base_id, title=None, param_key=None, visible=True, **kwargs
    ):

        if param_key is None:
            param_key = name

        self.input = dbc.Select(
            id={**base_id, "name": name, "param_key": param_key, "layer": "input"},
            **kwargs,
        )

        style = {"padding": "15px 0px 0px 0px"}
        if not visible:
            style["display"] = "none"

        super(DbcDropdownItem, self).__init__(
            title=title,
            title_id={
                **base_id,
                "name": name,
                "param_key": param_key,
                "layer": "label",
            },
            item=self.input,
            style=style,
        )


class DbcRadioItem(DbcControlItem):
    def __init__(
        self, name, base_id, title=None, param_key=None, visible=True, **kwargs
    ):

        if param_key is None:
            param_key = name

        self.input = dbc.RadioItems(
            id={**base_id, "name": name, "param_key": param_key, "layer": "input"},
            **kwargs,
        )

        style = {"padding": "15px 0px 0px 0px"}
        if not visible:
            style["display"] = "none"

        super(DbcRadioItem, self).__init__(
            title=title,
            title_id={
                **base_id,
                "name": name,
                "param_key": param_key,
                "layer": "label",
            },
            item=self.input,
            style=style,
        )


class DbcBoolItem(DbcControlItem):
    def __init__(
        self, name, base_id, title=None, param_key=None, visible=True, **kwargs
    ):

        if param_key is None:
            param_key = name

        self.input = dbc.Switch(
            id={**base_id, "name": name, "param_key": param_key, "layer": "input"},
            label=title,
            label_style={"margin": "0px 0px 0px 0px"},
            # input_style={"height": "36px"},
            **kwargs,
        )

        style = {"padding": "15px 0px 0px 0px"}
        if not visible:
            style["display"] = "none"

        super(DbcBoolItem, self).__init__(
            title="",  # title is already in the switch
            title_id={
                **base_id,
                "name": name,
                "param_key": param_key,
                "layer": "label",
            },
            item=self.input,
            style=style,
        )


class DbcParameterItems(dbc.Form):
    type_map = {
        "float": DbcNumberItem,
        "int": DbcNumberItem,
        "str": DbcStrItem,
        "slider": DbcSliderItem,
        "dropdown": DbcDropdownItem,
        "radio": DbcRadioItem,
        "bool": DbcBoolItem,
    }

    def __init__(self, _id, json_blob, values=None):
        super(DbcParameterItems, self).__init__(id=_id, children=[])
        self._json_blob = json_blob
        self.children = self.build_children(values=values)

    def _determine_type(self, parameter_dict):
        if "type" in parameter_dict:
            if parameter_dict["type"] in self.type_map:
                return parameter_dict["type"]
            elif parameter_dict["type"].__name__ in self.type_map:
                return parameter_dict["type"].__name__
        elif type(parameter_dict["value"]) in self.type_map:
            return type(parameter_dict["value"])
        raise TypeError(
            f"No item type could be determined for this parameter: {parameter_dict}"
        )

    def build_children(self, values=None):
        children = []
        for json_record in self._json_blob:
            # Build a parameter dict from self.json_blob
            type = json_record.get("type", self._determine_type(json_record))
            json_record = json_record.copy()
            if values and json_record["name"] in values:
                json_record["value"] = values[json_record["name"]]
            json_record.pop("type", None)
            # TODO: Use comp_group to fix training parameters and enable/disable parameters that
            # do not fall into the scope of the job (training, inference, etc.)
            if "comp_group" in json_record:
                json_record.pop("comp_group", None)
            item = self.type_map[type](**json_record, base_id=self.id)
            children.append(item)

        return children
