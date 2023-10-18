import board
import displayio
import busio
import adafruit_st7789
from adafruit_display_shapes.rect import Rect
import random
import time

# Release any resources currently in use for the displays
displayio.release_displays()

# Initialize SPI
spi = busio.SPI(clock=board.GP18, MOSI=board.GP19)

# Pimoroni Pico Display configuration and initialization
tft_cs = board.GP17
tft_dc = board.GP16
tft_reset = board.GP15

display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_reset)
display = adafruit_st7789.ST7789(display_bus, width=240, height=135, rowstart=40, colstart=53, rotation=270)

def generate_random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def lerp_color(start, end, fraction):
    """Interpolate between two colors."""
    r = int(start[0] + (end[0] - start[0]) * fraction)
    g = int(start[1] + (end[1] - start[1]) * fraction)
    b = int(start[2] + (end[2] - start[2]) * fraction)
    return (r, g, b)

# Setup squares
squares = []
current_colors = []
target_colors = []

group = displayio.Group()
for y in range(0, 120, 20):  # 6 rows
    for x in range(0, 240, 20):  # 12 columns
        color = generate_random_color()
        square = Rect(x, y, 20, 20, fill=color)
        squares.append(square)
        group.append(square)
        current_colors.append(color)
        target_colors.append(generate_random_color())

display.show(group)

STEPS = 100
PAUSE = 0.1

while True:
    for step in range(STEPS):
        for i, square in enumerate(squares):
            new_color = lerp_color(current_colors[i], target_colors[i], step / STEPS)
            square.fill = new_color
        time.sleep(PAUSE)

    current_colors = target_colors[:]
    target_colors = [generate_random_color() for _ in range(72)]
