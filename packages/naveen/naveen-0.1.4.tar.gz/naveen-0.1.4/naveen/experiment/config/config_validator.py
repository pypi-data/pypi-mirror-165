
class ConfigValidator(object):

    def __init__(self) -> None:
        pass

    @staticmethod
    def is_valid_config_file(config: dict) -> bool:

        required_fields = ["name", "reshaper", "plotter",
                           "experiment_module", "experiment_class"]

        for field in required_fields:
            assert field in config, "Counld not find field {}".format(field)

        assert " " not in config["name"], "Name cant have spaces"
        assert "/" not in config["name"], "Name cant have slashes"

        return True
