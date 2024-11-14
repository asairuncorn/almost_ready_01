# Set GPIO pins for switch, LED, and pump relay
SWITCH_PIN = 17  # GPIO pin for the start switch
LED_PIN = 27     # GPIO pin for the LED
RELAY_PIN = 22   # GPIO pin for the pump relay

# Set pump duration (in seconds)



from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import time
import RPi.GPIO as GPIO
from switch import Switch
from led import LED
from pump import Pump
from timer import Timer
from sensor import *
import threading
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_default_secret_key')  # Use environment variable or default key
socketio = SocketIO(app, cors_allowed_origins="*")




GPIO.setmode(GPIO.BCM)  # Set GPIO mode


def handle_sensor_data(data):
    """
    Handle sensor data by emitting or processing it.
    """

    # while self.pump_active:
    #     # Simulate the pressure readings (e.g., random data between 0-100)
    formatted_data = f"{data:.2f}"
    print(f"Emitted sensor data: {formatted_data}")
    #
    socketio.emit('pressure_sensor_reading_1', {'message': formatted_data})
    socketio.sleep(1)  # Sleep for 1 second bef





class PiPumpController:
    def __init__(self, switch_pin, led_pin, relay_pin, pump_duration, socket_io, callback):
        """
        Initializes the PiPumpController with all components.
        """
        self.callback = callback
        self.switch = Switch(switch_pin)
        self.led = LED(led_pin)
        self.pump = Pump(relay_pin)

        self.pump_active = False
        self.socketio = socket_io
        self.timer = Timer(pump_duration, data_callback=handle_sensor_data)




    def check_and_run(self):
        """
        Checks the switch and controls the pump, LED, and timer accordingly.
        """
        if self.switch.is_pressed():
            if not self.pump_active:
                print("Switch pressed. Activating pump.")
                #self.socketio.emit('switch_status', {'status': 'active'})  # Notify that switch is active
                self.start_pump()
        # else:
        #     if self.pump_active:
        #         print("Switch released. Deactivating pump.")
        #         self.stop_pump()
        #     else:
        #         # Emit "Install cartridge" status when switch is not pressed
        #         self.socketio.emit('switch_status', {'status': 'install_cartridge'})
        #         print("Switch not pressed. Install cartridge.")

    def start_pump(self):
        """
        Starts the pump, LED, and timer.
        """
        self.pump.on()
        self.led.set_green()
        self.pump_active = True

        self.timer.start()
        # self.handle_sensor_data(data)
        self.stop_pump()  # Automatically stop after timer ends

    def stop_pump(self):
        """
        Stops the pump and sets LED to yellow.
        """
        self.pump.off()
        self.led.set_yellow()
        self.pump_active = False

    def run(self):
        """
        Continuously checks the switch state to control the pump and LED.
        """
        print("Starting PiPumpController. Press Ctrl+C to exit.")
        try:
            while True:
                self.check_and_run()
                time.sleep(0.1)  # Delay to avoid excessive CPU usage
        except KeyboardInterrupt:
            print("\nExiting program.")
        finally:
            GPIO.cleanup()




# Serve the HTML page
@app.route('/')
def index():
    return render_template('index_c.html')


# # Countdown function that runs in a background thread
# def countdown_timer(button_id, duration=10):
#     seconds = duration
#     while seconds > 0:
#         # Emit remaining time to the client
#         socketio.emit('server_response', {'message': f'Time remaining for pump {button_id}: {seconds} s', 'button_id': button_id} )
#         sensor_1 = pressure_sensor_1()
#
#
#         socketio.emit('pressure_sensor_reading_1',
#                       {'message': sensor_1})
#         print(f"Time remaining for bay {button_id}: {seconds} seconds")  # Print for server logging
#         socketio.sleep(1)  # Non-blocking wait
#         seconds -= 1
#
#
#     # Notify client when time is up
#     socketio.emit('server_response', {'message': f"Pump is stopping... {button_id}!"})
#     #stop_pomp(button_id)
#     print(f"Pump {button_id} stopped!")


# Event handler for button presses

@socketio.on('start_pump')
def handle_pump(data):
    print("opis",data.get("blockId"))
    print('proces_time', data.get('proces_time'))
    time_process = data.get('proces_time')
    #pump_thread = threading.Thread(target=start_pump, args=(data.get("blockId"), data.get('proces_time')))
    #pump_thread.start()
    print("Pump started:", data)  # Log incoming data for debugging
    button_id = data.get("blockId")
    print("Button press event received:", button_id)


    pump_controller = PiPumpController(SWITCH_PIN, LED_PIN, RELAY_PIN, pump_duration=time_process, socket_io=socketio, callback=handle_sensor_data)
    #GPIO.set_pin_state(SWITCH_PIN, GPIO.HIGH)
    pump_controller.check_and_run()

    #countdown_timer(button_id, data.get('proces_time'))

    #duration = data.get('duration', 10)  # Default to 10 seconds if not specified


# Run the server using socketio.run for WebSocket support
if __name__ == '__main__':
    print("Starting Flask-SocketIO server...")
    socketio.run(app, host='127.0.0.1', port=5005, debug=True, allow_unsafe_werkzeug=True)




