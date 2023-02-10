import pytest
from mqhad.utils import Utils


class TestUtils:
    def test_check_type_failure(self):
        with pytest.raises(TypeError):
            Utils.check_type("1", int)

    def test_check_type_success(self):
        result = Utils.check_type(1, int)
        assert result == True
