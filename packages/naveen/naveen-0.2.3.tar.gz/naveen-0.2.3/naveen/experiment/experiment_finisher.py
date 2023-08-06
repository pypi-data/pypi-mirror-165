import subprocess
from naveen.experiment.config.abstract_config import AbstractConfig  # type: ignore # noqa: E501


class ExperimentFinisher(object):

    def __init__(self, config: AbstractConfig, results_directory: str):
        '''results directory is usually a unit timestamp'''
        self.config = config
        self.results_directory = results_directory

    def reshape(self) -> None:
        scriptargs = self.config.reshaper
        if self.config.reshaper == []:
            return None
        # e.g. ["python", "scripts/reshapers/demo.py"]
        command, script = scriptargs[0:2]
        assert script.startswith("scripts/reshaper/")
        subprocess.run(scriptargs + ["--results_directory", self.results_directory] + [  # noqa: E501
            "--results_file", self.config.name + ".csv"])

    def plot(self) -> None:

        scriptargs = self.config.plotter
        if self.config.plotter == []:
            return None
        # e.g. ["R", "scripts/plotters/demo.R"]
        command, script = scriptargs[0:2]
        assert script.startswith("scripts/plotter/")
        # for now assume that the plotter takes one arg,
        # which is self.config["name"] + ".reshaped.csv"
        subprocess.run(
            scriptargs + [self.results_directory + "/" + self.config.name + ".reshaped.csv"])  # noqa: E501

    def finish_results(self) -> None:
        self.reshape()
        self.plot()
