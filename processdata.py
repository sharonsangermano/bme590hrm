import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy import signal


class ProcessData:

    def __init__(self, data_table_arg):
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
        self.data_table = data_table_arg
        self.time = data_table_arg['Time']
        self.voltage = self.data_table['Voltage']
        self.corr = []
        self.corr_peaks = []
        self.num_beats = 0
        self.beats = []

    def get_data(self):
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

#def main():
#    data_in = pd.read_csv("test_data/test_data1.csv", names=['Time', 'Voltage'])
#    time = data_in['Time']
#    voltage = data_in['Voltage']
#    print(data_in)
#    print(time)
#    print(voltage)
#    min_voltage = min(voltage)
#    print(min_voltage)
#
#if __name__ == "__main__":
#    main()