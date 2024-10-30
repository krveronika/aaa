import pytest
from unittest.mock import patch
import json
from what_is_year_now import what_is_year_now


class TestWhatIsYearNow:

    @patch("urllib.request.urlopen")
    def test_ymd_format(self, mock_urlopen):
        mock_resp = {"currentDateTime": "2019-03-01"}
        # https://stackoverflow.com/questions/48113538/mocking-urllib-request-urlopens-read-function-returns-magicmock-signature
        mock_urlopen.return_value.__enter__.return_value.read.return_value = json.dumps(
            mock_resp
        )
        assert what_is_year_now() == 2019

    @patch("urllib.request.urlopen")
    def test_dmy_format(self, mock_urlopen):
        # Подготавливаем ответ API в формате DD.MM.YYYY
        mock_resp = {"currentDateTime": "01.03.2019"}
        mock_urlopen.return_value.__enter__.return_value.read.return_value = json.dumps(
            mock_resp
        )

        assert what_is_year_now() == 2019

    @patch("urllib.request.urlopen")
    def test_invalid_format(self, mock_urlopen):
        # Передаем неправильный формат даты
        mock_resp = {"currentDateTime": "invalid date format"}
        mock_urlopen.return_value.__enter__.return_value.read.return_value = json.dumps(
            mock_resp
        )
        with pytest.raises(ValueError):
            what_is_year_now()
