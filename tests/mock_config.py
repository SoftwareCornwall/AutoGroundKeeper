# -*- coding: utf-8 -*-
null = 0


class MockConfig:
    def __init__(self):
        self.data = {
            "interval": 10,
            "moisture_level_threshold": 800,
            "water_pumping_duration": 2,
            "water_not_detected_thresshold": 5,
            "water_detected_by_incress": 20,
            "water_detected_timeout": 5,
            "check_frequency": 5,
            "run_duration": null,
            "record_interval": 60,
            "tank_led_blink": 1,
            "max_moisture_level": 1000,
            "buzzer_on_time": 2,
            "buzzer_off_time": 3
        }

    def __getitem__(self, key):
        try:
            return self.data[key]
        except KeyError:
            return None
