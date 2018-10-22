import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy import signal
import math


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
        self.peaks = []

    def get_data(self):
        """
            Args:
            Attributes:
            Returns:
                data_table (list???):
        """
        #self.data_table = pd.read_csv(self.filename, names=['Time', 'Voltage'])
        #self.time = self.data_table['Time']
        #self.voltage = self.data_table['Voltage']
        #return self.data_table
        self.data_table = np.loadtxt(self.filename, delimiter=",")
        #self.time = self.data_table[:, 0]
        #self.voltage = self.data_table[:, 1]
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

    def get_min(self):
        return min(self.voltage)

    def get_max(self):
        return max(self.voltage)

    def get_duration(self):
        return max(self.time) - min(self.time)

    def get_peaks(self):
        voltage_series =  pd.Series(data = self.voltage)
        freq = 1/(self.time[1] - self.time[0])
        win_percent = 0.6
        moving_average = voltage_series.rolling(int(win_percent*freq)).mean()
        avg_voltage = (np.mean(voltage_series))
        moving_average = [avg_voltage if math.isnan(x) else x for x in moving_average]
        moving_average = [(x+abs(avg_voltage-abs(min(self.voltage)/2)))*1.2 for x in moving_average]
        window = []
        peaks = []
        location = 0
        for datapoint in voltage_series:
            rolling_mean = moving_average[location]
            if datapoint < rolling_mean and len(window) < 1:
                location += 1
            elif datapoint > rolling_mean:
                window.append(datapoint)
                location += 1
                if datapoint >= len(voltage_series):
                    beat_location = location - len(window) + (window.index(max(window)))
                    peaks.append(beat_location)
                    window = []
            else:
                beat_location = location - len(window) + (window.index(max(window)))
                peaks.append(beat_location)
                window = []
                location += 1
        self.peaks = peaks
        return self.peaks

    def get_num_beats(self):
        self.num_beats = len(self.peaks)
        return self.num_beats

    def get_beats_time(self):
        for i in self.peaks:
            if i <= len(self.time):
                self.beats.append(self.time[i])
        return self.beats

    def get_peak_voltage(self):
        for i in self.peaks:
            if i <= len(self.voltage):
                self.volts.append(self.voltage[i])
        return self.volts
