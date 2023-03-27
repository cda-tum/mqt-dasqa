from typing import Any, Union
import yaml


class Utils:
    @staticmethod
    def check_type(
        x, expected_class: Union[Any, list[Any]], raise_error: bool = True
    ) -> bool:
        if isinstance(expected_class, list) == False:
            expected_class = [expected_class]

        truth = [isinstance(x, expected_class_) for expected_class_ in expected_class]
        if any(truth) == False:
            if raise_error == True:
                raise TypeError(
                    "Expected object of type {} but got {}".format(
                        expected_class, type(x)
                    )
                )
            else:
                return False
        else:
            return True

    @staticmethod
    def load_yaml(path: str) -> dict:
        with open(path, "r") as f:
            return yaml.safe_load(f)
