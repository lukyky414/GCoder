from math import sqrt
from sys import stderr

class Printer:
    def __init__():
        #Parameters of the printer
        self.BED_SIZE_X = 220
        self.BED_SIZE_Y = 220
        self.TEMP_HOT_END = 200
        self.TEMP_BED = 70
        self.FAT_LINE_POSITION_Y = -5
        self.DISTANCE_AUTO_RETRACT = 10
        self.FILAMENT_DIAMETER = 1.75
        self.NOZZLE_DIAMETER = 0.4
        self.RETRACT_DISTANCE = 3
        self.Z_LIFTING = 1
        self.Y_FORWARDING = 180
        self.LAYER_HEIGHT = 0.15
        self.COOLDOWN = True
        self.SPEED_RETRACT = 200

        self._x = 0
        self._y = 0
        self._z = 0
        self._e = 0
        self.f = None
    
    #Move the hot end to position.
    # x, y, z -> the position. None : no change in axes
    # retract -> true: force retract, false: no retract, None: auto retract with distance
    def go_to(x=None, y=None, z=None, speed=1500, retract=None, z_lifting=False):
        if self.file is None:
            print("Please create a file with new_file before anything else", file=stderr)
            exit(1)
        if x is None:
            x = self._x
        if y is None:
            y = self._y
        if z is None:
            z = self._z
        
        e = self._e

        #Auto retract if distance is big
        if retract is None:
            distance = self._distance(x, y, z)
            if distance > self.DISTANCE_AUTO_RETRACT:
                retract = True
        
        #Retract & Z_lift
        if retract:
            e = e-self.RETRACT_DISTANCE
            self._go_to(self._x, self._y, self._z, e, self.SPEED_RETRACT)
        if z_lifting:
            z = z+self.Z_LIFTING
            self._go_to(self._x, self._y, z, e, speed)

        #Move
        self._go_to(x, y, z, e, speed)

        #Undo retract and z_lift
        if z_lifting:
            z = z-self.Z_LIFTING
            self._go_to(x, y, z, e, speed)
        if retract:
            e = e+self.RETRACT_DISTANCE
            self._go_to(x, y, z, e, self.SPEED_RETRACT)


    #Move the hot end to position and print plastic
    def print_to(x=None, y=None, z=None, speed=1000, flow_multiplier=1):
        if self.file is None:
            print("Please create a file with new_file before anything else", file=stderr)
            exit(1)
        if x is None:
            x = self._x
        if y is None:
            y = self._y
        if z is None:
            z = self._z
        
        d = self._distance(x, y, z)
        e = self._e + self._extruder_position(d) * flow_multiplier

        self._go_to(x, y, z, e)
    
    def _go_to(x, y, z, e, speed):

        self._x = x
        self._y = y
        self._z = z
        self._e = e

    
    def _distance(x, y, z):
        tot = (self._x - x)**2 + (self._y - y)**2 + (self._z - z)**2
        return sqrt(tot)


    #Get the position needed for the hot end to print
    def _extruder_position(distance):
        self.FILAMENT_DIAMETER
        self.NOZZLE_DIAMETER
        self.LAYER_HEIGHT

    #Create a new file, and automatically add the header
    def new_file(name):
        self.file = open(name, "w")
        self._file_header()

    #The header of the file
    def _file_header():
        #Home all axes (be sure to start heating in a good position)

        #Select the temperature needed, and wait to heat up
        self.TEMP_BED
        self.TEMP_HOT_END

        #Home all axes (before the print, in case of heat distortion)

        #Print a fat straight line to purge the Hot end
        self.FAT_LINE_POSITION_Y
        self.BED_SIZE_X/2

        #Reset the position of the extruder
        

    #End and close the file
    def end_file():
        if self.file is None:
            print("Please create a file with new_file before anything else", file=stderr)
            exit(1)
        self._file_footer()
        self.file.close()
        self.file = None

    #The footer of the file
    def _file_footer():
        #Retract a little
        self.RETRACT_DISTANCE

        #Go up a bit to avoid collision with the print
        self.Z_LIFTING

        #Home all to reset position

        #Go to high y, to move the print out and reachable
        self.Y_FORWARDING

        #Disable all steppers

        #Stop the heating
        if self.COOLDOWN
