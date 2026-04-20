import json
from unittest.mock import patch

import pandas
import pytest

from src.services import line_selection


@patch("pandas.read_excel")  # Заменяем pd.read_excel на mock
def test_line_selection(mock_read_excel):
    mock_data = {
        "Дата платежа": ["06.02.2021", "07.02.2021", "08.02.2021"],
        "Сумма платежа": [-138.0, 80.0, 100.0],
        "Категория": ["Супермаркеты", "Фастуфуд", "Бьюти"],
        "Описание": ["Колхоз", "ЗП", "АЗС"],
    }
    mock_df = pandas.DataFrame(mock_data)
    mock_read_excel.return_value = mock_df

    expected_result = json.dumps(
        [
            {
                "Дата платежа": "06.02.2021",
                "Сумма платежа": -138.0,
                "Категория": "Супермаркеты",
                "Описание": "Колхоз",
            }
        ],
        ensure_ascii=False,
    )
    assert line_selection(["Супермаркеты"]) == expected_result

    with pytest.raises(NameError):
        line_selection(a)

    with pytest.raises(TypeError):
        line_selection()
