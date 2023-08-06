import importlib
import json
import unittest
import os
import glob

from dataclasses import fields
from naveen.data.scrapers.html_tag_stripper import HTMLTagStripper
from naveen.experiment.config.dynamic_experiment_config_maker import DynamicExperimentConfigMaker  # noqa: E501
from naveen.experiment.config.experiment_group_parser import ExperimentGroupParser  # type: ignore # noqa: E501
from naveen.experiment.experiment_finisher import ExperimentFinisher
from naveen.experiment.experiment import DemoExperiment
from naveen.experiment.experiment_group_runner import ExperimentGroupRunner
from naveen.experiment.experiment_runner import ExperimentRunner
from naveen.experiment.experiment_writer import ExperimentWriter
from naveen.data.pipe_cleaner import PipeCleaner
from naveen.utils.ngram_maker import NgramMaker


def long_tests() -> None:
    os.system(
        "cat test/fixtures/url_list.txt | stream | wc -l > test/fixtures/output/stream2.txt")  # noqa: E501
    with open("test/fixtures/output/stream2.txt", "r") as inf:
        assert inf.read().strip() == "2"
    print("[*] Long tests passed")


class TestMethods(unittest.TestCase):

    def setUp(self) -> None:
        self.demo = 1
        maker = DynamicExperimentConfigMaker()
        self.config = maker.from_json("config/demo.json")
        for fn in glob.glob('test/fixtures/1659230924/*reshaped*'):
            os.remove(fn)
        for fn in glob.glob("test/fixtures/output/*"):
            os.remove(fn)

    def test_import_lib(self) -> None:
        module = importlib.import_module('naveen.experiment.experiment')
        my_class = getattr(module, 'DemoExperiment')
        my_instance = my_class(self.config)
        assert type(my_instance) == DemoExperiment

    def test_pipe_cleaner_true(self) -> None:
        cleaner: PipeCleaner = PipeCleaner(extension=".json", output_dir=".")
        exists = cleaner.already_exists("/tmp/a")
        self.assertFalse(exists)

    def test_pipe_cleaner_false(self) -> None:
        cleaner: PipeCleaner = PipeCleaner(
            extension=".json", output_dir="test/fixtures/config/")
        exists = cleaner.already_exists("test/fixtures/config/voss")
        self.assertTrue(exists)

    def test_demo(self) -> None:
        self.assertTrue(self.demo, 1)

    def test_demo_experiment_loads(self) -> None:
        demo_experiment = DemoExperiment(self.config)
        assert type(demo_experiment) == DemoExperiment

    def test_experiment_writer_loads(self) -> None:
        writer = ExperimentWriter(self.config)
        assert type(writer) == ExperimentWriter

    def test_experiment_runner(self) -> None:

        self.setUp()
        import sys
        sys.path.append("naveen")

        runner = ExperimentRunner(self.config,
                                  output_directory="test/fixtures/1659230924")

        runner.run()
        expected = "test/fixtures/1659230924/vossbooks.reshaped.csv"
        self.assertTrue(os.path.exists(expected))
        expected2 = "test/fixtures/1659230924/vossbooks.reshaped.pdf"
        self.assertTrue(os.path.exists(expected2))

    def test_exclusion_list(self) -> None:
        os.system("cat test/fixtures/url_list.txt | filter -e test/fixtures/exclusion_list.txt | wc -l > test/fixtures/output/exclusion1.txt")  # noqa: E501
        with open("test/fixtures/output/exclusion1.txt", "r") as inf:
            self.assertTrue(inf.read().strip(), "1")

    def test_dynamic_config_maker_json(self) -> None:
        maker = DynamicExperimentConfigMaker()
        config = maker.from_json("test/fixtures/config/voss.json")
        with open("test/fixtures/config/voss.json", "r") as inf:
            configdict = json.load(inf)
            names = [o.name for o in fields(config)]
            for k in configdict.keys():
                self.assertTrue(k in names)

    def test_dynamic_config_maker_yaml(self) -> None:
        maker = DynamicExperimentConfigMaker()
        config = maker.from_yaml("test/fixtures/config/voss.yaml")
        with open("test/fixtures/config/voss.json", "r") as inf:
            # voss.yaml and voss.json are identical
            configdict = json.load(inf)
            names = [o.name for o in fields(config)]
            for k in configdict.keys():
                self.assertTrue(k in names)

    def test_finisher_reshaper(self) -> None:
        expected = "test/fixtures/1659230924"
        expected = expected + "/" + "vossbooks.reshaped.csv"
        if os.path.exists(expected):
            os.remove(expected)

        res = "test/fixtures/1659230924"
        finisher = ExperimentFinisher(self.config,
                                      results_directory=res)
        finisher.reshape()
        assert os.path.exists(expected)

    def test_finisher_plotter(self) -> None:
        expected = "test/fixtures/1659230924" + "/" + "vossbooks.reshaped.csv"
        if os.path.exists(expected):
            os.remove(expected)
        dir_ = "test/fixtures/1659230924"
        finisher = ExperimentFinisher(self.config, results_directory=dir_)
        finisher.reshape()
        finisher.plot()

    def test_tag_stripper(self) -> None:
        # https://allnurses.com/hedis-nursing-t709251/
        # should remove the block quotes
        with open("test/fixtures/blockquote.html", "r") as inf:
            html = inf.read()

        tag_stripper = HTMLTagStripper(html, "blockquote")

        quoted = "was thinking of taking the coarse you mentioned abov"
        self.assertTrue(quoted not in tag_stripper.strip())

    def test_ngrammer(self) -> None:

        line = "I am a fish"

        ngram_maker = NgramMaker(n=2)

        ngrams = ngram_maker.get_ngrams_from_whitespace_delimited_text(line)

        self.assertTrue("I am" in ngrams)
        self.assertTrue("am a" in ngrams)
        self.assertTrue("a fish" in ngrams)
        self.assertTrue(len(ngrams) == 3)

    def test_experiment_group_parser_happy_path(self) -> None:
        parser = ExperimentGroupParser("config/experiment_groups/demo.yaml")
        configs = parser.parse_experiment_configs()
        self.assertEqual(len(configs), 8)  # 4 settings for dim, 2 models
        german = sum(1 for j in configs if  # type: ignore # noqa:E501 # can't be sure experiment config has model
                     j.model == "test/fixtures/models/de.gz")  # type: ignore # noqa:E501 # can't be sure experiment config has model
        english = sum(1 for j in configs if j.model ==  # type: ignore # noqa:E501 # can't be sure experiment config has model
                      "test/fixtures/models/en.gz")  # type: ignore # noqa:E501 # can't be sure experiment config has model
        d8 = sum(1 for j in configs if j.dimension == 8)  # type: ignore
        self.assertEqual(d8, 2), "Two experiments have dimension 8"  # type: ignore # noqa:E501
        self.assertEqual(german, 4), "Two experiments have German"   # type: ignore # noqa:E501
        self.assertEqual(english, 4), "Two experiments have English"   # type: ignore # noqa:E501
        d8_german = sum(1 for j in configs if j.dimension ==
                        8 and j.model == "test/fixtures/models/de.gz")
        self.assertEqual(d8_german, 1), "One experiment has d8 and is German"  # type: ignore # noqa:E501

    def test_experiment_group_parser_with_file_replacement(self) -> None:
        parser = ExperimentGroupParser(
            "config/experiment_groups/demo_file.yaml")
        configs = parser.parse_experiment_configs()
        self.assertEqual(len(configs), 8)  # 4 settings for dim, 2 models
        german = sum(1 for j in configs if  # type: ignore # noqa:E501 # can't be sure experiment config has model
                     j.model == "test/fixtures/models/de.gz")  # type: ignore # noqa:E501 # can't be sure experiment config has model
        english = sum(1 for j in configs if j.model ==  # type: ignore # noqa:E501 # can't be sure experiment config has model
                      "test/fixtures/models/en.gz")  # type: ignore # noqa:E501 # can't be sure experiment config has model
        d8 = sum(1 for j in configs if j.dimension == 8)  # type: ignore
        self.assertEqual(d8, 2), "Two experiments have dimension 8"  # type: ignore # noqa:E501
        self.assertEqual(german, 4), "Two experiments have German"   # type: ignore # noqa:E501
        self.assertEqual(english, 4), "Two experiments have English"   # type: ignore # noqa:E501
        d8_german = sum(1 for j in configs if j.dimension ==
                        8 and j.model == "test/fixtures/models/de.gz")
        self.assertEqual(d8_german, 1), "One experiment has d8 and is German"  # type: ignore # noqa:E501

    def test_experiment_group_runner_happy_path(self) -> None:
        import sys
        sys.path.append("naveen")
        runner = ExperimentGroupRunner("config/experiment_groups/demo.yaml")
        runner.run(outputdir="test/fixtures", package_name="experiment")

    def tearDown(self) -> None:
        os.system("rm -f Rplots.pdf")
        os.system("rm -rf test/fixtures/demogrou*")
        os.system("git checkout test/fixtures/1659230924/config.json")
        os.system("rm -f test/fixtures/1659230924/vossbooks.pdf")


if __name__ == '__main__':
    unittest.main()
