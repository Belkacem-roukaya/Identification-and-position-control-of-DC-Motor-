# import the require libraries
import utime
import RPi.GPIO as GPIO

# global variable
counter = 0

#constants
SAMPLING_TIME = 1 #(in second)

# interrupt handler function
def signal_handler(pin):
    global counter
    counter += 1

#GPIO configuration
GPIO.setmode(GPIO.BCM)

GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# attach the interrupt to the signal pin
GPIO.add_event_detect(5, GPIO.RISING , signal_handler)

# main
while true:
    utime.sleep(SAMPLING_TIME)

    revolution_per_sampling_time = counter / 12
    revolution_per_sec = revolution_per_sampling_time / SAMPLING_TIME
    revolution_per_minute = revolution_per_sec *60
     
    print("RPM : ", revolution_per_minute)

    # reset the counter to zero
    counter = 0
