import time
import board
import digitalio
import pwmio

# led = pwmio.PWMOut(board.LED, frequency=5000, duty_cycle=0)

PWM_PIN = [board.GP1, board.GP3, board.GP5, board.GP7]
DIR_PIN = [board.GP0, board.GP2, board.GP4, board.GP6]

PWM: pwmio.PWMOut = []
DIR: digitalio.DigitalInOut = []

# FL FR BL BR
SCALE = [-1, 1, -1, 1]

# Set up output pins
for pin in PWM_PIN:
    PWM.append(pwmio.PWMOut(pin, frequency=5000, duty_cycle=0))

for pin in DIR_PIN:
    dpin = digitalio.DigitalInOut(pin)
    dpin.direction = digitalio.Direction.OUTPUT
    DIR.append(dpin)

def allOff():
    for mot in PWM:
        mot.duty_cycle = 0

while True:
    try:
        val = input()
        vals = val.split(" ")
        for i in range(min(len(vals), 4)):
            v = float(vals[i]) * SCALE[i]
            print(f"Set val {i} to {int(abs(v) * 65535)}")
            PWM[i].duty_cycle = int(abs(v) * 65535)
            DIR[i].value = v > 0
    except Exception as e:
        print(e)
        allOff()