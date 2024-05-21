import unittest
from unittest.mock import patch, MagicMock

class TestEmployeeManagement(unittest.TestCase):

    @patch('mysql.connector.connect')
    def test_add_employee(self, mock_connect):
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        
        emp_mgmt = EmployeeManagement()
        with patch('builtins.input', side_effect=["123", "John Doe", "Manager", "50000"]):
            emp_mgmt.add_employee()
        
        mock_cursor.execute.assert_called()
        mock_connection.commit.assert_called()
        
    # Additional tests can be added for other methods

if __name__ == "__main__":
    unittest.main()
