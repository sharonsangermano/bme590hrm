import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy import signal


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
        self.corr = []
        self.corr_peaks = []
        self.num_beats = 0
        self.beats = []
        self.volts = []

    def get_data(self):
        """
            Args:
            Attributes:
            Returns:
                data_table (list???):
        """
        self.data_table = pd.read_csv(self.filename, names=['Time', 'Voltage'])
        self.time = self.data_table['Time']
        self.voltage = self.data_table['Voltage']
        return self.data_table

    def get_time(self):
        """
            Returns:
                time (list): list of time intervals from input file
        """
        return self.time

    def get_voltage(self):
        """
            Returns:
                voltage (list): list of voltages recorded in input file
        """
        return self.voltage

    def get_min(self):
        return min(self.voltage)

    def get_max(self):
        return max(self.voltage)

    def get_duration(self):
        return max(self.time) - min(self.time)

    def get_correlation(self):
        normalized = (self.voltage-np.min(self.voltage))/(np.max(self.voltage)-np.min(self.voltage))
        voltage_cen = normalized[0:300]
        self.corr = np.correlate(normalized, voltage_cen, 'full')
        print(len(self.corr))
        print(len(self.voltage))
        return self.corr

    def get_peaks(self):
        self.corr_peaks = signal.find_peaks_cwt(np.asarray(self.corr), np.arange(1,300))
        return self.corr_peaks

    def get_num_beats(self):
        self.num_beats = len(self.corr_peaks)
        return self.num_beats

    def get_beats_time(self):
        for i in self.corr_peaks:
            if i <= len(self.time):
                self.beats.append(self.time[i])
        return self.beats

    def get_peak_voltage(self):
        for i in self.corr_peaks:
            if i <= len(self.voltage):
                self.volts.append(self.voltage[i])
        return self.volts
