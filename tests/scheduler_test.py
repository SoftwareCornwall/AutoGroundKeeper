# -*- coding: utf-8 -*-
import unittest
import time

import scheduler


class CallRecording:
    def __init__(self):
        self.called = False

    def call(self):
        self.called = True


class TestScheduler(unittest.TestCase):
    def setUp(self):
        self.call_recording = CallRecording()
        self.schedule = scheduler.Scheduler()
        self.schedule.register_task(
            'call_function', self.call_recording.call, ())

    def tearDown(self):
        del self.call_recording
        del self.schedule

    def test_event_in_past_is_called(self):
        self.schedule.add_to_schedule('call_function', time.time() - 5)
        self.schedule.run_tasklist_once()
        self.assertTrue(self.call_recording.called)

    def test_event_in_future_is_not_called(self):
        self.schedule.add_to_schedule('call_function', time.time() + 60)
        self.schedule.run_tasklist_once()
        self.assertFalse(self.call_recording.called)

    def test_task_removed_from_schedule_after_use(self):
        self.schedule.add_to_schedule('call_function', time.time() - 5)
        self.assertEqual(1, len(self.schedule.schedule))
        self.schedule.run_tasklist_once()
        self.assertTrue(self.call_recording.called)
        self.assertEqual(0, len(self.schedule.schedule))


def test():
    unittest.main()


if __name__ == '__main__':
    test()
