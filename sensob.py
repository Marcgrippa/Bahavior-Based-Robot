class Sensob:

   # The main instance variables of a sensob are
   # a) its associated sensors and
   # b) its value
   # dict = {sensor1: value, sensor2: value2, ... , sensorn: valuen}
   associated_sensors_and_values = {}

   def __init__(self, sensors):
       for s in sensors:
           self.associated_sensors_and_values[s] = s.get_value()

   # The main method for a sensob is update, which should force the sensob
   # to fetch the relevant sensor value(s) and convert them into the pre-processed
   # sensob value
   def update(self):
       for s in self.associated_sensors_and_values:
           self.associated_sensors_and_values[s] = s.get_value()

