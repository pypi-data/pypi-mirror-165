from abc import ABC
from abc import abstractmethod
from typing import List
from naveen.experiment.config.abstract_config import AbstractConfig  # type: ignore # noqa: E501


class Experiment(ABC):

    def __init__(self, config: AbstractConfig):
        self.config = config

    @abstractmethod
    def get_results(self) -> List[dict]:
        pass


class DemoExperiment(Experiment):
    def get_results(self) -> List[dict]:
        if self.config.model == "test/fixtures/models/en.gz":  # type: ignore
            return [{"prod": "az", "hedonic": 8, "utilitatian": 9},
                    {"prod": "aa", "hedonic": 9, "utilitatian": 10}]
        elif self.config.model == "test/fixtures/models/de.gz":  # type: ignore
            return [{"prod": "az", "hedonic": 12, "utilitatian": 13},
                    {"prod": "aa", "hedonic": 14, "utilitatian": 15}]
        raise ValueError("Bad argument in self.config.model")
        return []  # for the linter
