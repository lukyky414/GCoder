from printer import Printer
from math import pi, cos, sin

def arc(printer, center, radius, start=0, stop=2*pi, slices=16):
    step_angle = (stop-start)/slices

    x = center[0] + cos(start)*radius
    y = center[1] + sin(start)*radius

    printer.go_to(x=x, y=y)

    angle = start

    while angle < stop:
        angle += step_angle

        x = center[0] + cos(angle)*radius
        y = center[1] + sin(angle)*radius

        printer.print_to(x=x, y=y)