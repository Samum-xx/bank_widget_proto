from unittest.mock import MagicMock, patch

from src.readers import read_csv, read_excel


class TestReadCSV:
    @patch("src.readers.Path")
    @patch("src.readers.open")
    @patch("src.readers.csv.DictReader")
    def test_read_csv_calls_open_and_dictreader(
        self, mock_dict_reader, mock_open, mock_path
    ):
        """Проверяет, что read_csv корректно использует open и csv.DictReader."""
        mock_path.return_value.exists.return_value = True

        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file

        mock_reader_instance = MagicMock()
        mock_reader_instance.__iter__.return_value = [
            {"amount": "100", "currency": "USD", "date": "2024-01-01"},
            {"amount": "200", "currency": "RUB", "date": "2024-01-02"},
        ]
        mock_dict_reader.return_value = mock_reader_instance

        result = read_csv("dummy_path.csv")

        mock_open.assert_called_once_with("dummy_path.csv", encoding="utf-8")
        assert len(result) == 2
        assert result[0]["amount"] == "100"
        assert result[1]["currency"] == "RUB"

    @patch("src.readers.Path")
    @patch("src.readers.open")
    @patch("src.readers.csv.DictReader")
    def test_read_csv_returns_list_of_dicts(
        self, mock_dict_reader, mock_open, mock_path
    ):
        """Убеждается, что функция возвращает именно список словарей."""
        mock_path.return_value.exists.return_value = True

        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file

        mock_reader_instance = MagicMock()
        mock_reader_instance.__iter__.return_value = [{"key": "value"}]
        mock_dict_reader.return_value = mock_reader_instance

        result = read_csv("test.csv")

        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], dict)


class TestReadExcel:
    @patch("src.readers.Path")
    @patch("src.readers.load_workbook")
    def test_read_excel_uses_load_workbook_and_active_sheet(
        self, mock_load_wb, mock_path
    ):
        """Проверяет, что read_excel корректно загружает книгу и берёт активный лист."""
        mock_path.return_value.exists.return_value = True

        mock_wb = MagicMock()
        mock_sheet = MagicMock()

        mock_header_cells = [MagicMock(value="amount"), MagicMock(value="currency")]
        mock_sheet.__getitem__.return_value = mock_header_cells

        row_1 = (100, "USD")
        row_2 = (200, "EUR")
        mock_sheet.iter_rows.return_value = [row_1, row_2]

        mock_wb.active = mock_sheet
        mock_load_wb.return_value = mock_wb

        result = read_excel("dummy_file.xlsx")

        mock_load_wb.assert_called_once_with("dummy_file.xlsx")
        assert len(result) == 2
        assert result[0] == {"amount": 100, "currency": "USD"}
        assert result[1] == {"amount": 200, "currency": "EUR"}

    @patch("src.readers.Path")
    @patch("src.readers.load_workbook")
    def test_read_excel_handles_empty_sheet(self, mock_load_wb, mock_path):
        """Проверка поведения на пустом листе."""
        mock_path.return_value.exists.return_value = True

        mock_wb = MagicMock()
        mock_sheet = MagicMock()

        mock_header_cells = [MagicMock(value="amount")]
        mock_sheet.__getitem__.return_value = mock_header_cells
        mock_sheet.iter_rows.return_value = []

        mock_wb.active = mock_sheet
        mock_load_wb.return_value = mock_wb

        result = read_excel("empty.xlsx")

        assert len(result) == 0
