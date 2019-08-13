
import time
import config_handler
import pump_control


class Watering_Schedule():

    def __init__(self, moist_sensor):
        self._config = config_handler.ConfigHandler()
        self.moisture_sensor = moist_sensor
        self.pump = pump_control.Pump()
        # vars set from config
        self.water_not_detected_thresshold = 0
        self.water_detected_by_incress = 0
        self.timeout = 0
        self.pumping_duration = 0
        self.update_from_config()

    def update_from_config(self):
        self.water_thresshold = self._config.data["water_not_detected_thresshold"]
        self.water_detected_by_incress = self._config.data["water_detected_by_incress"]
        self.timeout = self._config.data["water_detected_timeout"]

    def __enter__(self):
        self.pump.start_pump()
        return self

    def __exit__(self, type, value, traceback):
        self.pump.stop_pump()

    def enable_pump_until_moisture_sencor_is_saturated_for_duration(self):
        #        self.pump.start_pump()

        start_time = time.time()
        start_moist_value = self.moisture_sensor.get_moisture_a2d()
        current_moist_value = self.moisture_sensor.get_moisture_a2d()
        timedout = False

        print("Start moisture value: ", current_moist_value)

        while current_moist_value <= start_moist_value + self.water_thresshold:
            current_moist_value = self.moisture_sensor.get_moisture_a2d()
            time.sleep(0.1)    # sleep for 1/10 of a second.

            if start_time + self.timeout < time.time():
                timedout = True
                print("Error: Moisture Not Detected within timeout :(")
                break   # Error: we have not recived water with in the timeout :|

        print("Final moisture value: ", current_moist_value)

        if not timedout:
            time.sleep(self._config.data["water_pumping_duration"])

#        self.pump.stop_pump()

    def run(self):
        pass
