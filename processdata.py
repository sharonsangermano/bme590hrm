import pandas as pd
import numpy as np
import math
import logging
import readdata

class ProcessData:

    def __init__(self, file_arg):
        """Initialized an object of teh ProcessData class for the data file of interest.

        Args:
            file_arg: name of test data file to be analyzed

        Attributes:
            self.time: list of all time values obtained from the data file
            self.voltage: list of all voltage values obtained from the data file
            self.num_beats: the number of heart beats detected
            self.peaks: list of indices from the time and voltage array which indicate a peak in the voltage reading
            self.beats: list of times where peaks/beats occur
            self.volts: list of voltages at peak/beat
            self.duration: duration found for time/voltage data used to calculate mean heart rate
            self.mean_hr: mean heart rate calculated for the data set
        """
        self.time, self.voltage = readdata.get_data(file_arg)
        self.num_beats = 0
        self.peaks = []
        self.beats = []
        self.volts = []
        self.duration = 0
        self.mean_hr = 0
        self.min_vol = 0
        self.max_vol = 0
        logging.basicConfig(filename="hrm_log.txt", format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')

    def get_time(self):
        """

        Returns:
            time: list of all time values obtained from the data file

        """
        return self.time

    def get_voltage(self):
        """

        Returns:
            voltage: list of all voltage values obtained from the data file

        """
        return self.voltage

    def get_min(self):
        """

        Returns:
            min_vol: the minimum voltage from the data set

        """
        self.min_vol = min(self.voltage)
        return self.min_vol

    def get_max(self):
        """

        Returns:
            max_vol: the maximum voltage from the data set

        """
        self.max_vol = max(self.voltage)
        return self.max_vol

    def get_peaks(self):
        """

        Attributes:
            voltage_series:

        Returns:
            peaks: list of indices from the time and voltage array which indicate a peak in the voltage reading

        References:
            Modified from:
                van Gent, P. (2016). Analyzing a Discrete Heart Rate Signal Using Python. A tech blog about fun
                things with Python and embedded electronics. Retrieved from:
                http://www.paulvangent.com/2016/03/15/analyzing-a-discrete-heart-rate-signal-using-python-part-1/

            Author states that code may be modified and redistributed as long as the modified
            code is shared with the same right and the original author is cited using the format above.
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

    def get_results(self):
        results = {'Mean heart rate': round(self.mean_hr, 3),
                   'Minimum voltage': self.min_vol,
                   'Maximum voltage': self.max_vol,
                   'Duration': self.duration,
                   'Number of beats': self.num_beats,
                   'Beat occurrence times': self.beats,
                   }
        return results
