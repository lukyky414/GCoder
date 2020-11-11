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


        self._x = 0
        self._y = 0
        self._z = 0
        self._e = 0
    
    #Move the hot end to position.
    # X, Y, Z -> the position. None : no change in axes
    # retract -> true: force retract, false: no retract, None: auto retract with distance
    def go_to(X=None, Y=None, Z=None, speed=1500, retract=None, z_lifting=False):


        if distance > self.DISTANCE_AUTO_RETRACT

        self.RETRACT_DISTANCE
        self.Z_LIFTING

    #Move the hot end to position and print plastic
    def print_to(X=None, Y=None, Z=None, speed=1000):

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

        #Go to high Y, to move the print out and reachable
        self.Y_FORWARDING

        #Disable all steppers

        #Stop the heating
        if self.COOLDOWN
