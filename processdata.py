import pandas as pd
import numpy as np
import math
import logging
import readdata

class ProcessData:

    #def __init__(self, time_arg, voltage_arg):
    def __init__(self, file_arg):
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
        self.time, self.voltage = readdata.get_data('test_data/test_data1.csv')
        #self.time = time_arg
        #self.voltage = voltage_arg
        self.corr = []
        self.corr_peaks = []
        self.num_beats = 0
        self.beats = []
        self.volts = []
        self.peaks = []
        self.mean_hr = 0
        self.duration = 0
        logging.basicConfig(filename="hrm_log.txt", format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')

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

    def get_peaks(self):
        """
        Modified from:
            van Gent, P. (2016). Analyzing a Discrete Heart Rate Signal Using Python. A tech blog about fun
            things with Python and embedded electronics. Retrieved from:
            http://www.paulvangent.com/2016/03/15/analyzing-a-discrete-heart-rate-signal-using-python-part-1/

        Author states that code may be modified and redistributed as long as the modified
            code is shared with the same right and the original author is cited using the format above.
        :return:
        """
        voltage_series = pd.Series(data=self.voltage)
        freq = 1/(self.time[1] - self.time[0])
        win_percent = 0.5
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

    def get_duration(self):
        self.duration = max(self.beats) - min(self.beats)
        return self.duration

    def get_mean_hr(self):
        self.mean_hr = self.num_beats/self.duration*60
        if self.mean_hr < 40:
            logging.warning('Warning: Heart rate abnormally low. (<40 bmp)')
        if self.mean_hr > 180:
            logging.warning('Warning: Heart rate abnormally high. (>180 bmp)')
        return self.mean_hr


# class ProcessData:
#
#     def __init__(self, time_arg, voltage_arg):
#         """
#             Args:
#                 filename_arg (string): name of ECG file to open
#
#             Attributes:
#                 self.filename (string): name of ECG file to open
#                 self.data_table (tuple??list??): stores time and voltage data from file
#                 self.time (list): stores time data from file
#                 self.voltage (list): stores voltage data from file
#                 self.corr (list): stores correlated voltage data
#                 self.corr_peaks (list): stores list index of where peaks occur
#                 self.num_beats (int): the number of beats found in the ECG file
#                 self.beats (list): time of each beat
#
#             Returns:
#         """
#         self.time = time_arg
#         self.voltage = voltage_arg
#         self.corr = []
#         self.corr_peaks = []
#         self.num_beats = 0
#         self.beats = []
#         self.volts = []
#         self.peaks = []
#         self.mean_hr = 0
#         self.duration = 0
#         logging.basicConfig(filename="hrm_log.txt", format='%(asctime)s %(message)s',
#                             datefmt='%m/%d/%Y %I:%M:%S %p')
#
#     def get_time(self):
#         """
#             Returns:
#                 time (list): list of time intervals from input file
#         """
#         return self.time
#
#     def get_voltage(self):
#         """
#             Returns:
#                 voltage (list): list of voltages recorded in input file
#         """
#         return self.voltage
#
#     def get_min(self):
#         return min(self.voltage)
#
#     def get_max(self):
#         return max(self.voltage)
#
#     def get_duration(self):
#         self.duration = max(self.time) - min(self.time)
#         return self.duration
#
#     def get_peaks(self):
#         """
#         Modified from:
#             van Gent, P. (2016). Analyzing a Discrete Heart Rate Signal Using Python. A tech blog about fun
#             things with Python and embedded electronics. Retrieved from:
#             http://www.paulvangent.com/2016/03/15/analyzing-a-discrete-heart-rate-signal-using-python-part-1/
#
#         Author states that code may be modified and redistributed as long as the modified
#             code is shared with the same right and the original author is cited using the format above.
#         :return:
#         """
#         voltage_series = pd.Series(data=self.voltage)
#         freq = 1/(self.time[1] - self.time[0])
#         win_percent = 0.5
#         moving_average = voltage_series.rolling(int(win_percent*freq)).mean()
#         avg_voltage = (np.mean(voltage_series))
#         moving_average = [avg_voltage if math.isnan(x) else x for x in moving_average]
#         moving_average = [(x+abs(avg_voltage-abs(min(self.voltage)/2)))*1.2 for x in moving_average]
#         window = []
#         peaks = []
#         location = 0
#         for datapoint in voltage_series:
#             rolling_mean = moving_average[location]
#             if datapoint < rolling_mean and len(window) < 1:
#                 location += 1
#             elif datapoint > rolling_mean:
#                 window.append(datapoint)
#                 location += 1
#                 if datapoint >= len(voltage_series):
#                     beat_location = location - len(window) + (window.index(max(window)))
#                     peaks.append(beat_location)
#                     window = []
#             else:
#                 beat_location = location - len(window) + (window.index(max(window)))
#                 peaks.append(beat_location)
#                 window = []
#                 location += 1
#         self.peaks = peaks
#         return self.peaks
#
#     def get_num_beats(self):
#         self.num_beats = len(self.peaks)
#         return self.num_beats
#
#     def get_beats_time(self):
#         for i in self.peaks:
#             if i <= len(self.time):
#                 self.beats.append(self.time[i])
#         return self.beats
#
#     def get_peak_voltage(self):
#         for i in self.peaks:
#             if i <= len(self.voltage):
#                 self.volts.append(self.voltage[i])
#         return self.volts
#
#     def get_mean_hr(self):
#         self.mean_hr = self.num_beats/self.duration*60
#         if self.mean_hr < 40:
#             logging.warning('Warning: Heart rate abnormally low. (<40 bmp)')
#         if self.mean_hr > 180:
#             logging.warning('Warning: Heart rate abnormally high. (>180 bmp)')
#         return self.mean_hr
