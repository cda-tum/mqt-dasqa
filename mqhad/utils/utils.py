from typing import Any

class Utils:
    @staticmethod
    def check_type(x, expected_class: Any) -> bool:
        if not isinstance(x, expected_class):
            raise TypeError(
                "Expected object of type {} but got {}".format(expected_class, type(x))
            )
        else:
            return True
