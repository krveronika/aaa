import pytest
from morse import decode, MORSE_TO_LETTER


class TestIssues02:

    @pytest.mark.parametrize(
        "input_str, expected_output",
        [
            (".- -... -.-.", "ABC"),
            ("... --- ...", "SOS"),
            (
                "-- .- .. -....- .--. -.-- - .... --- -. -....- ..--- ----- .---- ----.",
                "MAI-PYTHON-2019",
            ),
        ],
    )
    def test_decode_ok(self, input_str, expected_output):
        assert decode(input_str) == expected_output

    @pytest.mark.parametrize("input_str", ["1", "a", "#"])
    def test_decode_unsupport_symb(self, input_str):
        with pytest.raises(KeyError):
            decode(input_str)

    def test_decode_same_size(self):
        assert len(set(MORSE_TO_LETTER.keys())) == len(set(MORSE_TO_LETTER.values()))


class TestIssues02_bas_example:
    @pytest.mark.parametrize("input_str, expected_output", [(".-  -... -.-.", "A BC")])
    def test_decode_with_space(self, input_str, expected_output):
        assert decode(input_str) == expected_output
