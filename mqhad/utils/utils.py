class Utils:
    @staticmethod
    def check_type(x, expected_class):
        if not isinstance(x, expected_class):
            raise TypeError(
                "Expected object of type {} but got {}".format(expected_class, type(x))
            )
