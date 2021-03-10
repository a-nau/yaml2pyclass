[![build](https://github.com/a-nau/yaml2pyclass/workflows/build/badge.svg)](https://github.com/a-nau/yaml2pyclass/actions)
[![test](https://github.com/a-nau/yaml2pyclass/workflows/test/badge.svg)](https://github.com/a-nau/yaml2pyclass/actions)

# yaml2pyclass Code Generator

This package enables you to easily generate and instantiate dataclasses from an input `YAML` file. For example
this `YAML` file

```yaml
image_size: [ 1280, 960 ]
cluster_config:
  eps: 0.02
  min_num_samples: 10
path_output: "./ouput"
```

automatically converts to a Python `class`

```python
import dataclasses
import yaml2pyclass

class Config(yaml2pyclass.CodeGenerator):
    @dataclasses.dataclass
    class ClusterConfigClass:
        eps: float
        min_num_samples: int

    image_size: list
    cluster_config: ClusterConfigClass
    path_output: str
```

In addition to code creation, an instance of the generated class that is initialized with the `YAML`s values can be
created automatically.

The use case it was primarily developed for is facilitating code completion for arbitrary `YAML` config files.
Using `YAML` files as input config allows flexible and general information passing, however, when using [`pyyaml`](https://pypi.org/project/PyYAML/) the
information is saved as a `dict` which does not support any automatic code completion. This means, that you need to know
the exact variable names for access.

Using this package you can enjoy `YAML`s flexibility and generality, while additionally providing the benefit of code
completion and type specific suggestions from your IDE. Thus, no need to memorize exact variable names or types.

## Installation

You can install the package using `pip`

```shell
pip install git+https://github.com/a-nau/yaml2pyclass.git@latest
```

You can also download the [latest version](https://github.com/a-nau/yaml2pyclass/archive/latest.tar.gz) as `.tar.gz`
from Github and install it with
`pip install PATH/TO/latest.tar.gz`

Note that you can also add this to your project's `requirements.txt`

```shell
git+https://github.com/a-nau/yaml2pyclass.git@latest
```

## Usage

### File Update

To update an existing file, as e.g. in the case of a config file, you need to create a base file. The base file should
simply contain a class, that inherits from the `yaml2pyclass` base class `CodeGenerator`:

```python
import yaml2pyclass


class Config(yaml2pyclass.CodeGenerator):
    pass
```

Then, in the function where you want to use this class based on the `YAML` input, import the created class and call
the `from_yaml` function

```python
from path.to.config import Config

config = Config.from_yaml("config.yaml")
```

This will update the file of the `Config` class with dataclass that matches the input `YAML`.

## Contributors

This project is a collaboration with [Felix Hertlein](https://github.com/FelixHertlein).

## License

This code is distributed under the 3-Clause BSD License, see [LICENSE](LICENSE).


