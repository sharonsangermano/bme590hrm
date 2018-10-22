import numpy as np


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

    def get_data(self):
        """
            Args:
            Attributes:
            Returns:
                data_table (list???):
        """
        self.data_table = np.loadtxt(self.filename, delimiter=",")
        return self.data_table

    def get_time(self):
        """
            Returns:
                time (list): list of time intervals from input file
        """
        self.time = self.data_table[:, 0]
        return self.time

    def get_voltage(self):
        """
            Returns:
                voltage (list): list of voltages recorded in input file
        """
        self.voltage = self.data_table[:, 1]
        return self.voltage
