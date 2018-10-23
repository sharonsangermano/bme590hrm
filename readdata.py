import numpy as np
import sys

class ReadData:

    def __init__(self, filename_arg):
        """
            Args:
                filename_arg (string): name of ECG file to open

            Attributes:
                self.filename (string): name of ECG file to open
                self.data_table (tuple??list??): stores time and voltage data from file
                self.time (list): stores time data from file
                self.voltage (list): stores voltage data from file
                self.corr (list): stores correlated voltage data
                self.corr_peaks (list): stores list index of where peaks occur
                self.num_beats (int): the number of beats found in the ECG file
                self.beats (list): time of each beat

            Returns:
        """
        self.filename = filename_arg
        self.data_table = []
        self.time = []
        self.voltage = []

    def can_float(self, value):
        try:
            float(value)
            return True

        except ValueError:
            print('None float value found in dataset.  Skipping this time, voltage pair')
            return False

    def get_data(self):
        """
            Args:
            Attributes:
            Returns:
                data_table (list???):
        """
        try:
            self.data_table = np.loadtxt(self.filename, delimiter=",")

        except IOError:
            print("That file could not be found.  Please try again")
            sys.exit()

        for index in self.data_table:
            if self.can_float(index[0]) and self.can_float(index[1]):
                self.time.append(index[0])
                self.voltage.append(index[1])
        return self.time, self.voltage

        # index = 0
        # if index < len(self.input_data)
        #     if self.can_float(self.input_data[index, 0]) and self.can_float(self.input_data[index, 1])
        #         self.data_table.append([self.input_data[index, 0], self.input_data[index, 1]])
        #     index += 1
        # return self.data_table
