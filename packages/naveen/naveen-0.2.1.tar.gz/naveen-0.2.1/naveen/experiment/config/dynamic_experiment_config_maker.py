from dataclasses import make_dataclass
from typing import List
import json
import yaml  # type: ignore # mypy can't find library
from typing import Tuple
from typing import Any

from naveen.experiment.config.config_validator import ConfigValidator


class DynamicExperimentConfigMaker(object):

    def from_yaml(self, config_file: str) -> dict:
        assert config_file.endswith(".yaml") or config_file.endswith(".yml")
        with open(config_file, 'r') as yaml_input:
            yaml_config_as_dict: dict = yaml.safe_load(yaml_input)
            yaml_config_as_dict["filename"] = config_file
        return self._make_config_object(yaml_config_as_dict)  # type: ignore

        # figuring out type anno here is too hard

    def from_json(self, config_file: str):  # type: ignore

        assert config_file.endswith(".json")
        with open(config_file, "r") as inf:
            json_config_as_dict = json.load(inf)
            json_config_as_dict["filename"] = config_file
        return self._make_config_object(json_config_as_dict)  # type: ignore

    def _make_config_object(self, config):  # type: ignore # types confusing
        validator: ConfigValidator = ConfigValidator()
        assert validator.is_valid_config_file(config)

        # https://stackoverflow.com/questions/52534427/dynamically-add-fields-to-dataclass-objects
        fields: List[Tuple[str, Any]] = []
        fields.append(("name", str))
        fields.append(("reshaper", List[str]))
        fields.append(("plotter", List[str]))
        for k, v in config.items():
            if k not in ["name", "reshaper", "plotter"]:
                fields.append((k, type(v)))

        X = make_dataclass('DynamicConfig', fields)

        # https://www.reddit.com/r/learnpython/comments/9h74no/convert_dict_to_dataclass/
        return X(**config)
