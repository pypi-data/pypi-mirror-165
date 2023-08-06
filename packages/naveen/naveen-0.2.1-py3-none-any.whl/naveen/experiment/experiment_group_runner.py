from pathlib import Path
import time
import os
import sys

from naveen.experiment.config.experiment_group_parser import ExperimentGroupParser  # noqa: E501
from naveen.experiment.experiment_runner import ExperimentRunner  # type: ignore # noqa: E501


class ExperimentGroupRunner(object):

    def __init__(self, config_path: str,  # type: ignore
                 group_directory=None) -> None:  # type: ignore
        assert config_path.endswith("yaml") or config_path.endswith(
            "yml"), "Experiment group config must be yaml"
        self.config_path = config_path
        self.group_config = ExperimentGroupParser(
            group_config_filename=self.config_path)
        self.experiment_configs = self.group_config.parse_experiment_configs()
        group_name = self.group_config.get_group_name()
        if group_directory is None:
            self.group_directory = group_name + str(int(time.time()))
        else:
            self.group_directory = group_directory

    def get_path_to_results(self, outputdir: str) -> str:
        path_to_results = os.path.join(outputdir, self.group_directory)
        return path_to_results

    def prepare_path_to_results(self, path_to_results: str) -> None:
        Path(path_to_results).mkdir(parents=True, exist_ok=True)
        # write group config to root directory
        os.system("cp {} {}".format(self.config_path, path_to_results))

    def run(self, outputdir: str, package_name: str) -> None:

        path_to_results = self.get_path_to_results(outputdir)
        self.prepare_path_to_results(path_to_results=path_to_results)

        for ex_no, experiment_config in enumerate(self.experiment_configs):
            path_to_result = os.path.join(outputdir,
                                          self.group_directory,
                                          str(ex_no))
            runner = ExperimentRunner(experiment_config,
                                      package_name=package_name,
                                      output_directory=path_to_result)
            runner.run()


if __name__ == "__main__":
    runner = ExperimentGroupRunner("config/experiment_groups/demo.yaml")
    package_name = "naveen"
    sys.path.append(package_name)
    runner.run(outputdir="tmp", package_name=package_name)
    # rm -rf tmp/demogroup
