
import time
import config_handler

class Watering_Schedule():
    
    def __init__(self, moist_sensor, pum):
        self._config = config_handler.ConfigHandler()
        self.moisture_sensor = moist_sensor
        self.pump = pum
        # vars set from config
        self.water_not_detected_thresshold = 0
        self.water_detected_by_incress = 0
        self.timeout = 0
        self.pumping_duration
        self.update_from_config()
        
    def update_from_config(self):
        self.water_thresshold = self._config.data["water_not_detected_thresshold"]
        self.water_detected_by_incress = self._config.data["water_detected_by_incress"]
        self.timeout = self._config.data["water_detected_timeout"]
    
    def enable_pump_until_moisture_sencor_is_saturated_for_duration(self):
        self.pump.start_pump()
        
        start_time = time.time()
        start_moist_value = self.moisture_sensor.get_a2d_count();

        while self.moisture_sensor.get_a2d_count() <= start_moist_value + self.water_thresshold:
            time.sleep(0.1)    # sleep for 1/10 of a second.

            if start_time + self.timeout < time.time():
                print("Error: Moisture Not Detected within timeout :(")
                break   # Error: we have not recived water with in the timeout :|


        print("Final moisture value: ", self.moisture_sensor.get_a2d_count())

        time.sleep(self._config.data["water_pumping_duration"])

        self.pump.stop_pump()
        
    def run(self):
        pass