import RPi.GPIO as GPIO
import time

# Define the GPIO pins connected to the stepper motor
PINS = [14, 15, 18, 23]

# Define the sequence for full stepping
STEP_SEQUENCE = [
    [1, 0, 0, 1],
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
]

# define global var that stores what step the motor is on and what degree it is supposed to be on
current_step = 0
current_assumed_degrees = 0

# Setup GPIO mode
GPIO.setmode(GPIO.BCM)

# Setup GPIO pins as output
for pin in PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)


def step_motor(step):
    # Activate the GPIO pins according to the step
    for i in range(4):
        GPIO.output(PINS[i], step[i])


def stepper_rotate_deg(degrees_rotation, direction):
    # Set the sequence direction
    if direction == 'CCW':
        sequence = STEP_SEQUENCE[::-1]
    elif direction == 'CW':
        sequence = STEP_SEQUENCE
        degrees_rotation = -degrees_rotation
    else:
        print("Invalid direction. Please use 'CW' or 'CCW'.")
        return

    # Rotate the stepper motor a specific number of degrees in the specified direction.
    # since 512 does not divide into 360, we must alternate between rotating 7 and 9 steps
    steps_per_revolution = 512
    steps_per_degree = steps_per_revolution / 360

    # use global variable current_step to calculate current_degree

    global current_step
    global current_assumed_degrees
    target_step = round((current_assumed_degrees + degrees_rotation) * steps_per_degree)

    # Calculate the number of steps to move
    steps_to_move = target_step - current_step

    # Rotate the motor, need abs so the loop runs when negative
    for i in range(abs(steps_to_move)):
        for step in sequence:
            step_motor(step)
            time.sleep(0.005)  # Adjust this delay to control speed

    # Turn off the motor to save power
    for pin in PINS:
        GPIO.output(pin, 0)

    # update info on current step
    current_step += steps_to_move

    # update current assumed degrees
    current_assumed_degrees += degrees_rotation

    print(current_step, current_assumed_degrees)


def keep_cw_time(start_time=time.time()):
    # start time is the unix start time, and must be after current time
    time_now = time.time()

    if time_now > start_time:
        start_time = time_now

    # all times are rounded to the nearest 60 to keep minutes distinct
    previous_time = start_time // 60 * 60
    while True:
        current_time = time.time() // 60 * 60
        min_diff = int(current_time - previous_time)
        if min_diff >= 60:
            for i in range(0, min_diff // 60):
                stepper_rotate_deg(6, 'CW')
            previous_time = current_time


def continual_adjust(angle, times, direction):
    for i in range(times):
        stepper_rotate_deg(angle, direction)
        time.sleep(1)

    # keep_cw_time()


# stepper_rotate_deg(6, 'CCW')
# time.sleep(1)
# stepper_rotate_deg(24, 'CW')
continual_adjust(6, 60, "CW")

GPIO.cleanup()

