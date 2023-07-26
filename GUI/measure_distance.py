#import RPi.GPIO as GPIO
import time

from PyQt5.QtCore import pyqtSignal, QThread

# #GPIO Mode (BOARD / BCM)
# GPIO.setmode(GPIO.BCM)
#
# #set GPIO Pins rear
# GPIO_TRIGGER_REAR = 18
# GPIO_ECHO_REAR = 24
#
# #set GPIO direction (IN / OUT)
# GPIO.setwarnings(False)
# GPIO.setup(GPIO_TRIGGER_REAR, GPIO.OUT)
# GPIO.setup(GPIO_ECHO_REAR, GPIO.IN)
#
# #set GPIO Pins front
# GPIO_TRIGGER_FRONT = 17
# GPIO_ECHO_FRONT = 25
#
# #set GPIO direction (IN / OUT)
# GPIO.setwarnings(False)
# GPIO.setup(GPIO_TRIGGER_FRONT, GPIO.OUT)
# GPIO.setup(GPIO_ECHO_FRONT, GPIO.IN)



global running

def distance_front():
    # # set Trigger to HIGH
    # GPIO.output(GPIO_TRIGGER_FRONT, True)
    #
    # # set Trigger after 0.01ms to LOW
    # time.sleep(0.00001)
    # GPIO.output(GPIO_TRIGGER_FRONT, False)
    #
    # StartTime = time.time()
    # StopTime = time.time()
    #
    # # save StartTime
    # while GPIO.input(GPIO_ECHO_FRONT) == 0:
    #     StartTime = time.time()
    #
    # # save time of arrival
    # while GPIO.input(GPIO_ECHO_FRONT) == 1:
    #     StopTime = time.time()
    #
    # # time difference between start and arrival
    # TimeElapsed = StopTime - StartTime
    # # multiply with the sonic speed (34300 cm/s)
    # # and divide by 2, because there and back
    # distance = (TimeElapsed * 34300) / 2
    #
    # return distance
    return 0

class start_run_front(QThread):
    update_progress_signal = pyqtSignal(int)

    def run(self):
        global running
        running = True
        try:
            while running:
                dist_front = distance_front()
                self.update_progress_signal.emit(dist_front)
                time.sleep(1)
        except KeyboardInterrupt:
            print("Measurement stopped by User")
            # GPIO.cleanup()

def distance_rear():
    # # set Trigger to HIGH
    # GPIO.output(GPIO_TRIGGER_REAR, True)
    #
    # # set Trigger after 0.01ms to LOW
    # time.sleep(0.00001)
    # GPIO.output(GPIO_TRIGGER_REAR, False)
    #
    # StartTime = time.time()
    # StopTime = time.time()
    #
    # # save StartTime
    # while GPIO.input(GPIO_ECHO_REAR) == 0:
    #     StartTime = time.time()
    #
    # # save time of arrival
    # while GPIO.input(GPIO_ECHO_REAR) == 1:
    #     StopTime = time.time()
    #
    # # time difference between start and arrival
    # TimeElapsed = StopTime - StartTime
    # # multiply with the sonic speed (34300 cm/s)
    # # and divide by 2, because there and back
    # distance = (TimeElapsed * 34300) / 2
    #
    # return distance
    return 0

class start_run_rear(QThread):
    update_progress_signal = pyqtSignal(int)

    def run(self):
        global running
        running = True
        try:
            while running:
                dist_rear = distance_rear()
                self.update_progress_signal.emit(dist_rear)
                time.sleep(1)
        except KeyboardInterrupt:
            print("Measurement stopped by User")
            # GPIO.cleanup()


class kill_th():
    def __init__(self):
        super().__init__()
        global running
        running = False

if __name__ == '__main__':
    print(1)
    # thread = start_run()
    # thread.start()
