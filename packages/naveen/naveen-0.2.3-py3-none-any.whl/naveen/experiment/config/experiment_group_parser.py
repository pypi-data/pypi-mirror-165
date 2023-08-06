from collections import defaultdict
from copy import deepcopy
import itertools
from typing import List
import yaml  # type: ignore

from naveen.experiment.config.dynamic_experiment_config_maker import DynamicExperimentConfigMaker  # type: ignore # noqa: E501
from naveen.experiment.config.experiment_setting import ExperimentSetting


class ExperimentGroupParser(object):

    def get_experiment_template_kind(self, template: str) -> str:
        if template.endswith("yaml"):
            return "yaml"
        elif template.endswith("json"):
            return "json"
        else:
            msg = "Only json and yaml configs supported, you gave {}"
            raise ValueError(msg.format(template))

    def get_experiment_config(self, experiment_template: str):  # type: ignore
        experiment_config_parser = DynamicExperimentConfigMaker()
        experiment_config_type = self.get_experiment_template_kind(
            experiment_template)
        if experiment_config_type == 'yaml':
            experiment_config = experiment_config_parser.from_yaml(
                experiment_template)
        elif experiment_config_type == 'json':
            experiment_config = experiment_config_parser.from_json(
                experiment_template)
        return experiment_config

    def load_yaml_config(self, group_config_filename: str) -> dict:
        errormessage: str = "Group config must be yaml"
        assert group_config_filename.endswith(
            "yaml") or group_config_filename.endswith("yml"), errormessage

        # config/experiment_groups/demo.yaml
        with open(group_config_filename, 'r') as yaml_input:
            group_config: dict = yaml.safe_load(yaml_input)
            group_config["filename"] = group_config_filename
        return group_config

    def parse_settings(self, group_config: dict) -> List[List]:
        output = defaultdict(list)
        for setting in group_config["settings"]:
            if setting["type"] == "replacement":
                for value in setting["values"]:
                    experiment_setting = ExperimentSetting(field=setting['field'],  # noqa: E501
                                                           value=value)
                    output[setting["field"]].append(experiment_setting)
            if setting['type'] == "range":
                start = setting["start"]
                end = setting["end"]
                step = setting["step"]
                for value in range(start, end, step):
                    experiment_setting = ExperimentSetting(field=setting["field"],  # noqa: E501
                                                           value=value)
                    output[setting["field"]].append(experiment_setting)
            if setting["type"] == "file":  # the values are listed in a path
                # this is helpful for $ find -type f > path_to/options.txt
                path_to: str = setting["path"]
                with open(path_to, "r") as inf:
                    for value in inf:
                        value = value.replace("\n", "")
                        experiment_setting = ExperimentSetting(field=setting["field"],  # noqa: E501
                                                               value=value)
                        output[setting["field"]].append(experiment_setting)

        settings: List[List] = list(output.values())  # list of lists
        return settings

    def __init__(self, group_config_filename: str) -> None:
        self.group_config = self.load_yaml_config(group_config_filename)
        self.experiment_config = self.get_experiment_config(
            self.group_config["experiment_template"])

    def get_group_name(self) -> str:
        return self.group_config["group_name"]

    # returns list of experiment configs
    def parse_experiment_configs(self) -> list:
        settings = self.parse_settings(self.group_config)  # type: ignore
        possible_experiment_configs: List = [
            i for i in itertools.product(*settings)]
        experiment_configs: list = []
        for experiment_config in possible_experiment_configs:
            new_experiment_config = deepcopy(self.experiment_config)
            for setting in experiment_config:
                setattr(new_experiment_config,
                        setting.field, setting.value)
            experiment_configs.append(new_experiment_config)
        return experiment_configs


if __name__ == "__main__":
    parser = ExperimentGroupParser("config/experiment_groups/demo.yaml")
    for c in parser.parse_experiment_configs():
        print(c)
