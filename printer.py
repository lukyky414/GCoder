from math import sqrt, pi
from sys import stderr

class Printer:
    def __init__():
        #Parameters of the printer
        self.TEMP_HOT_END = 200
        self.TEMP_BED = 70
        self.BED_SIZE_X = 220
        self.BED_SIZE_Y = 220
        self.FAT_LINE_POSITION_Y = -5
        self.DISTANCE_AUTO_RETRACT = 10
        self.FILAMENT_DIAMETER = 1.75
        self.NOZZLE_DIAMETER = 0.4
        self.Z_LIFTING = None
        self.Y_FORWARDING = 180
        self.LAYER_HEIGHT = 0.15
        self.COOLDOWN = True
        self.RETRACT_DISTANCE = 3
        self.RETRACT_SPEED = 200
        # True: force retract at each movement, False: no retract, None: auto retract with distance
        self.RETRACT = None
        self.EXTRUDER_MULTIPLIER = 4
        self.ENABLE_FAN = True
        self.MOVEMENT_SPEED = 3600
        self.PRINT_SPEED = 1500
        self.PRINT_SPEED_FIRST_LAYER = 1000

        self._filament_surface = None

        self._first_layer = True
        self._x = 0
        self._y = 0
        self._z = 0
        self._e = 0
        self._file = None
    
    #Move the hot end to position.
    # x, y, z -> the position. None : no change in axes
    
    def go_to(x=None, y=None, z=None):
        if self._file is None:
            print("Please create a file with new_file before anything else", file=stderr)
            exit(1)
        if x is None:
            x = self._x
        if y is None:
            y = self._y
        if z is None:
            z = self._z
        
        e = self._e

        retract = self.RETRACT

        #Auto retract if distance is big
        if retract is None:
            distance = self._distance(x, y, z)
            if distance > self.DISTANCE_AUTO_RETRACT:
                retract = True
        
        #Retract & Z_lift
        if retract:
            e = e-self.RETRACT_DISTANCE
            self._go_to(self._x, self._y, self._z, e, self.RETRACT_SPEED)
        if self.Z_LIFTING is not None:
            z = z+self.Z_LIFTING
            self._go_to(self._x, self._y, z, e, self.MOVEMENT_SPEED)

        #Move
        self._go_to(x, y, z, e, self.MOVEMENT_SPEED)

        #Undo retract and z_lift
        if self.Z_LIFTING is not None:
            z = z-self.Z_LIFTING
            self._go_to(x, y, z, e, self.MOVEMENT_SPEED)
        if retract:
            e = e+self.RETRACT_DISTANCE
            self._go_to(x, y, z, e, self.RETRACT_SPEED)


    #Move the hot end to position and print plastic
    def print_to(x=None, y=None, z=None):
        if self._file is None:
            print("Please create a file with new_file before anything else", file=stderr)
            exit(1)
        if x is None:
            x = self._x
        if y is None:
            y = self._y
        if z is None:
            z = self._z
        
        d = self._distance(x, y, z)
        e = self._e + self._extruder_position(d)


        self._go_to(x, y, z, e, self.PRINT_SPEED)
    
    #Move up to a new layer
    def new_layer():
        if self._first_layer:
            self._first_layer = False
            if self.ENABLE_FAN:
                print("M106 S255", file=self._file)
        
        self._go_to(self._x, self._y, self._z+self.LAYER_HEIGHT, self._e, self.MOVEMENT_SPEED)
    
    def _go_to(x, y, z, e, speed):
        print("G1 X"+x+" Y"+y+" Z"+z+" E"+e+" F"+speed, file=self._file)

        self._x = x
        self._y = y
        self._z = z
        self._e = e

    
    def _distance(x, y, z):
        tot = (self._x - x)**2 + (self._y - y)**2 + (self._z - z)**2
        return sqrt(tot)


    #Get the position needed for the hot end to print
    def _extruder_position(distance):
        if self._filament_surface is None:
            self._filament_surface = pi * self.FILAMENT_DIAMETER**2
        
        volume = distance * self.LAYER_HEIGHT * self.NOZZLE_DIAMETER
        fil_length = volume / self._filament_surface
        size_to_print = fil_length * self.EXTRUDER_MULTIPLIER

        return self._e + size_to_print

    #Create a new file, and automatically add the header
    def new_file(name):
        self._file = open(name, "w")
        self._file_header()

    #The header of the file
    def _file_header():
        #Absolute positionning
        print("G90", file=self._file)

        #Home all axes (be sure to start heating in a good position)
        print("G28 X0 Y0", file=self._file)
        self._x = 0
        self._y = 0

        #Select the temperature needed
        print("M104 S"+self.TEMP_HOT_END, file=self._file)
        print("M140 S"+self.TEMP_BED, file=self.file)
        #and wait to heat up
        print("M109 S"+self.TEMP_HOT_END, file=self._file)
        print("M190 S"+self.TEMP_BED, file=self.file)

        #Home all axes (before the print, in case of heat distortion)
        print("G28 X0 Y0 Z0", file=self._file)
        self._x = 0
        self._y = 0
        self._z = 0

        #Reset the position of the extruder to be sure its 0
        print("G92 E0", file=self._file)
        self._e = 0

        #Print a fat straight line to purge the Hot end
        self._go_to(0, self.FAT_LINE_POSITION_Y, self.LAYER_HEIGHT, 0, 1500)

        d = self._distance(self.BED_SIZE_X, self.FAT_LINE_POSITION_Y, self.LAYER_HEIGHT)
        e = self._extruder_position(d)*2
        self._go_to(self.BED_SIZE_X, self.FAT_LINE_POSITION_Y, self.LAYER_HEIGHT, e, 900)

        #Reset the position of the extruder (begin file with e = 0)
        print("G92 E0", file=self._file)
        self._e = 0

        self._first_layer = True
        self._filament_surface = None

    #End and close the file
    def end_file():
        if self._file is None:
            print("Please create a file with new_file before anything else", file=stderr)
            exit(1)
        self._file_footer()
        self._file.close()
        self._file = None

    #The footer of the file
    def _file_footer():
        #disable the fan
        print("M107", file=self._file)

        #Retract a little
        self._go_to(self._x, self._y, self._z, self._e-self.RETRACT_DISTANCE, self.RETRACT_SPEED)

        #Go up a bit to avoid collision with the print
        self._go_to(self._x, self._y, self._z+self.Z_LIFTING, self._e, 1500)

        #Home x and y axis to reset position
        print("G28 X0 Y0", file=self._file)
        self._x = 0
        self._y = 0

        #Go to high y, to move the print out and reachable
        self._go_to(0, self.Y_FORWARDING, self._z, self._e, 1500)

        #Disable all steppers
        print("M18 X Y Z E", file=self._file)

        #Stop the heating
        if self.COOLDOWN:
            print("M104 S0", file=self._file)
            print("M140 S0", file=self._file)
            
