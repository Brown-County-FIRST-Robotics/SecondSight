
import unittest
import tempfile
import SecondSight.config

import os
import json

class TestConfig(unittest.TestCase):

    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.config_object = SecondSight.config.Configuration()

        self.config_data = {
            "item1": 1,
            "item2": "2",
            "item3": [1, 2, 3]
        }

        self.config_file = os.path.join(self.tempdir.name, "config.json")
        with open(self.config_file, "w") as out_fh:
            json.dump(self.config_data, out_fh)
        self.config_object.set_path(self.config_file)

    def tearDown(self):
        self.tempdir.cleanup()

    def testSingleton(self):
        new_object = SecondSight.config.Configuration()
        self.assertEqual(self.config_object, new_object)

    def testConfigOpen(self):
        file_path = self.config_object.file_path
        self.assertTrue(os.path.exists(file_path))
        self.assertEqual(file_path, self.config_file)

    def testNoConfig(self):
        new_tempdir = tempfile.TemporaryDirectory()

        self.config_object.close()
        config_path = os.path.join(new_tempdir.name, "config.json")
        self.config_object.set_path(config_path)
        self.assertEqual(self.config_object.get_value("cameras")[0]["port"], 0)

        self.assertIsNone(self.config_object.get_value("not_real"))

        new_tempdir.cleanup()

    def testConfigClose(self):
        
        self.config_object.set_value("new_item", "new_value")
        
        file_path = self.config_object.file_path
        self.config_object.close()
        self.assertTrue(os.path.exists(file_path))

        self.config_object.set_path(file_path)
        self.assertEqual(self.config_object.get_value("new_item"), "new_value")

    def testConfigSetGet(self):
        self.config_object.set_value("test_item", "test_value")
        self.assertEqual(self.config_object.get_value("test_item"), "test_value")
        self.assertIsNone(self.config_object.get_value("not_real_value"))

    def testComplexConfig(self):
        complex_config = {
            "one": 1,
            "two": 2,
            "arr": ["pirate"]

        }

        self.config_object.set_value("complex", complex_config)
        
        file_path = self.config_object.file_path
        self.config_object.close()
        self.config_object.set_path(file_path)

        complex_read = self.config_object.get_value("complex")

        self.assertEqual(complex_config["one"], complex_read["one"])
        self.assertEqual(complex_config["two"], complex_read["two"])
        self.assertEqual(complex_config["arr"], complex_read["arr"])

    def testConfigGetAll(self):
        all_config = self.config_object.get_all()
        self.assertEqual(all_config, self.config_data)