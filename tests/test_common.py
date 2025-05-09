import unittest
import os
import tempfile
from src.common.versioning import DataVersioning
from src.common.config import Config
from src.common.db import Database
from src.common.utils import Utils
from datetime import datetime
from pathlib import Path

class TestDataVersioning(unittest.TestCase):
    def setUp(self):
        self.versioner = DataVersioning()
        self.test_data = {
            'timestamp': datetime.now().isoformat(),
            'total_urls': 10,
            'urls': ['http://example.com/1', 'http://example.com/2']
        }

    def test_version_data(self):
        version = self.versioner.version_bulk_data(self.test_data)
        self.assertIsInstance(version, str)
        self.assertTrue(version.startswith('v'))

    def test_get_version_path(self):
        version = 'v1.0.0'
        path = self.versioner.get_version_path(version)
        self.assertIsInstance(path, Path)
        self.assertTrue(str(path).endswith(version))

class TestConfig(unittest.TestCase):
    def setUp(self):
        self.config = Config()

    def test_load_config(self):
        config = self.config.load()
        self.assertIsInstance(config, dict)
        self.assertIn('database', config)
        self.assertIn('logging', config)

    def test_get_database_config(self):
        db_config = self.config.get_database_config()
        self.assertIsInstance(db_config, dict)
        self.assertIn('host', db_config)
        self.assertIn('port', db_config)
        self.assertIn('database', db_config)

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = Database()

    def test_connect(self):
        connection = self.db.connect()
        self.assertIsNotNone(connection)
        connection.close()

    def test_execute_query(self):
        result = self.db.execute_query("SELECT 1")
        self.assertIsNotNone(result)

class TestUtils(unittest.TestCase):
    def setUp(self):
        self.utils = Utils()

    def test_clean_text(self):
        text = "  Test  Text  "
        cleaned = self.utils.clean_text(text)
        self.assertEqual(cleaned, "Test Text")

    def test_validate_email(self):
        valid_email = "test@example.com"
        invalid_email = "not-an-email"
        self.assertTrue(self.utils.validate_email(valid_email))
        self.assertFalse(self.utils.validate_email(invalid_email))

    def test_validate_phone(self):
        valid_phone = "1234567890"
        invalid_phone = "not-a-phone"
        self.assertTrue(self.utils.validate_phone(valid_phone))
        self.assertFalse(self.utils.validate_phone(invalid_phone))

if __name__ == '__main__':
    unittest.main() 