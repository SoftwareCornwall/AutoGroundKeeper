import unittest
import csv_recording


class TestCSV(unittest.TestCase):
    def test_rows_ordered_by_time_from_CSV_data(self):
        # most recent readings at end of file
        CSV_handler = csv_recording.CSVRecording()
        list_of_datetimes = CSV_handler.read_data(1)
        self.assertEqual(sorted(list_of_datetimes[0]), list_of_datetimes[0])

    def test_moisture_values_are_in_range_of_0_to_1023(self):
        CSV_handler = csv_recording.CSVRecording()
        list_of_datetimes = CSV_handler.read_data(1)
        self.assertGreaterEqual(1023, sorted(list_of_datetimes[1])[0])
        self.assertLessEqual(0, sorted(list_of_datetimes[1])[-1])

    def test_light_levels_are_inrange_of_0_to_1023(self):
        CSV_handler = csv_recording.CSVRecording()
        list_of_datetimes = CSV_handler.read_data(2)
        self.assertGreaterEqual(1023, sorted(list_of_datetimes[1])[0])
        self.assertLessEqual(0, sorted(list_of_datetimes[1])[-1])
