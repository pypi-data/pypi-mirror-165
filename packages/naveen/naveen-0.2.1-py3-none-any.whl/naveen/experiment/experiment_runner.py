import importlib
from naveen.experiment.experiment_finisher import ExperimentFinisher
from naveen.experiment.experiment_writer import ExperimentWriter
from naveen.experiment.config.abstract_config import AbstractConfig  # type: ignore  # noqa: E501


class ExperimentRunner(object):

    def __init__(self, config: AbstractConfig,
                 package_name: str = None,  # e.g. src or experiment; name of base package # noqa: E501
                 output_directory: str = None) -> None:  # type: ignore
        self.config = config

        module = importlib.import_module(
            config.experiment_module, package=package_name)
        # figuring out types for next line seems hard and not worth it
        experiment = getattr(module, config.experiment_class)  # type: ignore
        self.experiment = experiment(config)
        self.output_directory = output_directory

    def run(self) -> None:

        if self.output_directory is None:
            writer = ExperimentWriter(self.config)
        else:
            writer = ExperimentWriter(self.config, self.output_directory)
        out = writer.output_directory
        finisher = ExperimentFinisher(self.config,
                                      results_directory=out)
        results = self.experiment.get_results()
        writer.write_results(results)
        finisher.finish_results()
        print("[*] Write results to {}".format(writer.output_directory))
