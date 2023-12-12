import inspect
import os
import re
from dataclasses import dataclass
from inspect import getmembers
from pathlib import Path
from typing import Any, Dict, List

import yaml


@dataclass
class CodeGenerator:
    @classmethod
    def from_yaml(cls, config_file: str) -> "CodeGenerator":
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Could not find YAML file at {config_file}")
        with open(config_file, "r") as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
            data = {} if data is None else data

        cls._update_code(data)

        old_fields = list(
            [value for key, value in getmembers(cls) if key == "__dataclass_fields__"][
                0
            ].keys()
        )
        dummy_data = {field: None for field in old_fields}

        c = cls(**dummy_data)
        cls._update_data(c, data)

        return c

    @classmethod
    def _update_data(cls, obj: object, data: Dict[str, Any]) -> object:

        obj.__dict__.clear()
        obj.__dict__.update(data)

        for key, value in data.items():
            if not isinstance(value, dict):
                continue

            subclass = type(cls._to_class_name(key), (), {})
            obj.__dict__[key] = cls._update_data(subclass(), value)

        return obj

    @classmethod
    def _update_code(cls, data: Dict[str, Any]) -> None:
        code_file = Path(inspect.getfile(cls))
        lines = code_file.read_text().split("\n")

        start_pos_list = [
            idx
            for idx, line in enumerate(lines)
            if ("class" in line and cls.__name__ in line and "Class" not in line)
        ]
        if len(start_pos_list) != 1:
            raise ValueError("Malformed config file! Cannot modify file!")

        # find indentation
        pos = start_pos_list[0] + 1
        match = re.match(pattern=r"^(?P<indentation>\s+)", string=lines[pos])
        if match is None:
            raise ValueError("Malformed config file! Cannot modify file!")
        indentation = match.groupdict()["indentation"]

        # clear old keys
        while pos < len(lines):
            lines.pop(pos)

        # add new keys
        lines[pos:pos] = [
            indentation + line for line in cls._create_code(data, indentation)
        ] + [""]

        # add import
        cls._add_import(lines)

        code_file.write_text("\n".join(lines))

    @classmethod
    def _add_import(cls, lines: List[str]) -> None:
        pattern = r"^\s*import\s*dataclasses\s*$"
        if any(re.match(pattern=pattern, string=line) for line in lines):
            return

        lines.insert(0, "import dataclasses")

    @classmethod
    def _create_code(cls, data: Dict[str, Any], indentation: str) -> List[str]:
        if len(data.keys()) == 0:
            return ["pass"]

        dict_keys = [key for key, value in data.items() if isinstance(value, dict)]

        lines = []
        for key in dict_keys:
            lines.append("@dataclasses.dataclass")
            lines.append(f"class {cls._to_class_name(key)}:")
            lines.extend(
                [
                    indentation + line
                    for line in cls._create_code(data[key], indentation)
                ]
            )
            lines.append("")

        for key, value in data.items():
            if key in dict_keys:
                lines.append(f"{str(key)}: {cls._to_class_name(key)}")
            else:
                if isinstance(value, str) and 'type___' in value:
                    new_type = value.split('type___')[1]
                    lines.append(f"{str(key)}: {new_type}")
                else:
                    lines.append(f"{str(key)}: {type(value).__name__}")

        return lines

    @staticmethod
    def _to_class_name(key: str) -> str:
        return "".join(x.title() for x in key.split("_")) + "Class"
