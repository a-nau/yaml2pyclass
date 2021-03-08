import unittest
import yaml

from tests.demo_config import Config


class Yaml2ConfigTest(unittest.TestCase):
    def setUp(self) -> None:
        self.path_config = "tests/config.yaml"

    def test(self):
        data_class = Config.from_yaml(self.path_config)
        with open(self.path_config, "r") as file:
            data_yaml = yaml.load(file, Loader=yaml.FullLoader)
        self.assertTrue(self.compare_yaml_dict_and_generated_class(data_yaml, data_class))

    def compare_yaml_dict_and_generated_class(self, data_yaml, data_class) -> bool:
        equal = True
        for key, val_yaml in data_yaml.items():
            val_class = data_class.__getattribute__(key)
            if isinstance(val_yaml, dict):
                equal = equal and self.compare_yaml_dict_and_generated_class(val_yaml, val_class)
            else:
                equal = equal and (val_yaml == val_class)
        return equal
