# timer.py
import time
from sensor import*

class Timer:
    def __init__(self, duration, data_callback=None):
        """
        Initializes the timer with a specified duration in seconds.
        """
        self.pressure_sensor = PresureSensor()



        self.duration = duration
        self.remaining_time = duration
        self.data_callback = data_callback


        


    def start(self):
        """
        Starts the countdown timer and displays the remaining time.
        """
        start_time = time.time()
        while time.time() - start_time < self.duration:
            self.remaining_time = self.duration - int(time.time() - start_time)
            print(f"Time remaining: {self.remaining_time} seconds", end='\r')
            time.sleep(1)

            s_data = self.pressure_sensor.read_data()
            self.data_callback(s_data)


            # print("\n --")
            # if self.data_callback:
            #     self.data_callback(s_data)
            #
            #
            # print(s_data)


        print("\nTimer completed.")



