import pytest
from one_hot_encoder import fit_transform


class TestOneHotEncoder:
    @pytest.mark.parametrize(
        "input_val, expected_vals",
        [
            (["a"], [("a", [1])]),
            ([], []),
            (
                ["Moscow", "New York", "Moscow", "London"],
                [
                    ("Moscow", [0, 0, 1]),
                    ("New York", [0, 1, 0]),
                    ("Moscow", [0, 0, 1]),
                    ("London", [1, 0, 0]),
                ],
            ),
        ],
    )
    def test_fit_transform_with_simple_data(self, input_val, expected_vals):
        assert fit_transform(input_val) == expected_vals

    def test_raises_type_error_on_empty_input(self):
        with pytest.raises(TypeError):
            fit_transform()

    def test_type_error_on_int_arg(self):
        with pytest.raises(TypeError):
            fit_transform(1, 2, 3)
