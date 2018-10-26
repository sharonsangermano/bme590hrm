import pandas as pd
import numpy as np
import math
import logging
import readdata


class ProcessData:

    def __init__(self, file_arg):
        """Initialized an object of teh ProcessData class for the data
        file of interest.

        Args:
            file_arg: name of test data file to be analyzed

        Attributes:
            self.time: list of all time values obtained from the
                        data file
            self.voltage: list of all voltage values obtained from the
                        data file
            self.num_beats: the number of heart beats detected
            self.peaks: list of indices from the time and voltage array
                        which indicate a peak in the voltage reading
            self.beats: list of times where peaks/beats occur
            self.volts: list of voltages at peak/beat
            self.duration: duration found for time/voltage data
                        used to calculate mean heart rate
            self.mean_hr: mean heart rate calculated for the data set

        Returns:

        Raises:
            IOError: If file_name is not the correct file name

        """
        logging.basicConfig(filename="hrm_log.txt", format='%(asctime)s '
                                                           '%(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
        self.file_name = file_arg
        try:
            self.time, self.voltage = readdata.get_data(self.file_name)
        except IOError as inst:
            raise inst
        logging.info('Successfully imported data from: %s ' % self.file_name)
        self.num_beats = 0
        self.peaks = []
        self.beats = []
        self.volts = []
        self.duration = 0
        self.mean_hr = 0
        self.min_vol = 0
        self.max_vol = 0

    def check_neg(self):
        """
        Checks voltage list to determine if all values are negative

        Returns:
            boolean: True if the list contains one or more positive
                    voltage values.  False if the list contains only
                    negative voltage values

        """
        for x in self.voltage:
            if x > 0:
                return True
        return False

    def handle_neg(self):
        """
        Checks if the current voltage list is all negative. If
        all negative, adds 1.5V to each voltage value and logs
        a warning

        Returns:
            voltage: list containing voltages -- updated if needed

        """
        if self.check_neg() is False:
            for y in range(0, len(self.voltage)):
                self.voltage[y] = self.voltage[y] + 1.5
                logging.warning('Warning: No positive voltages detected. '
                                'all voltage values shifted up 1.5V. Minimum '
                                'and maximum voltage values may not be '
                                'accurate')
        return self.voltage

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
        logging.info('Successfully identified minimum voltage.')
        return self.min_vol

    def get_max(self):
        """

        Returns:
            max_vol: the maximum voltage from the data set

        """
        self.max_vol = max(self.voltage)
        logging.info('Successfully identified maximum voltage.')
        return self.max_vol

    def get_peaks(self):
        """
        Using moving average algorithm to detect voltage peaks and
        captures the time[] and voltage[] indices corresponding to
        each peak.

        Attributes:
            voltage_series: pandas series of the voltage list
            freq: frequency of voltage readings
            win_percent: window size as a fraction of of the sample frequency
            moving_average: moving average of voltages
            avg_voltage: average voltage of data series
            window: current window being analyzed
            peaks: time index of peaks detected
            peak_len: number of peaks detected

        Returns:
            peaks: list of indices from the time and voltage array which
                    indicate a peak in the voltage reading

        References:
            Modified from:
                van Gent, P. (2016). Analyzing a Discrete Heart Rate Signal
                Using Python. A tech blog about fun things with Python and
                embedded electronics. Retrieved from:
                http://www.paulvangent.com/2016/03/15/analyzing-a-discrete-
                heart-rate-signal-using-python-part-1/

            Author states that code may be modified and redistributed as long
            as the modified code is shared with the same right and the original
            author is cited using the format above.
        """
        voltage_series = pd.Series(data=self.voltage)
        freq = 1 / (self.time[1] - self.time[0])
        win_percent = 0.5
        moving_average = voltage_series.rolling(int(win_percent * freq)).mean()
        avg_voltage = (np.mean(voltage_series))
        moving_average = [avg_voltage if math.isnan(x) else x for x in
                          moving_average]
        moving_average = [(x + abs(avg_voltage - abs(min(self.voltage) / 2))) *
                          1.2 for x in moving_average]
        window = []
        peaks = []
        peak_len = 0
        while peak_len is 0:
            location = 0
            for datapoint in voltage_series:
                rolling_mean = moving_average[location]
                if datapoint < rolling_mean and len(window) < 1:
                    location += 1
                elif datapoint > rolling_mean:
                    window.append(datapoint)
                    location += 1
                    if datapoint >= len(voltage_series):
                        beat_location = location - len(window) + \
                                        (window.index(max(window)))
                        peaks.append(beat_location)
                        window = []
                else:
                    beat_location = location - len(window) + \
                                    (window.index(max(window)))
                    peaks.append(beat_location)
                    window = []
                    location += 1
                peak_len = len(peaks)
            for x in range(0, len(voltage_series)):
                voltage_series[x] = voltage_series[x] * -1
            if peak_len == 0:
                logging.warning('Warning: Inverted ECG signal detected '
                                'peaks detected using inversion of input')
        self.peaks = peaks
        logging.info('Successfully identified ECG voltage peaks.')
        return self.peaks

    def get_num_beats(self):
        """
        Beats are considered to be one peak to the next so the
        total number of beats is one fewer than the total number of
        peaks detected.

        Returns:
            num_beats: number of heart beats detected

        """
        self.num_beats = len(self.peaks) - 1
        logging.info('Successfully identified number of heart beats.')
        if self.num_beats < 5:
            logging.warning('Warning: Less than 5 beats detected. Mean '
                            'heart rate may be inaccurate.')
        return self.num_beats

    def get_beats_time(self):
        """

        Returns:
            beats: list of times corresponding to peaks detected

        """
        for i in self.peaks:
            if i <= len(self.time):
                self.beats.append(self.time[i])
        logging.info('Successfully identified times corresponding to beats.')
        return self.beats

    def get_peak_voltage(self):
        """

        Returns:
            volts: list of voltages corresponding to peaks detected

        """
        for i in self.peaks:
            if i < len(self.voltage):
                self.volts.append(self.voltage[i])
        logging.info('Successfully identified voltages corresponding with '
                     'beats.')
        return self.volts

    def get_duration(self):
        """
        Duration is considered the time from the first detected peak
        to the last detected peak.

        Returns:
            duration: the time in which the detected beats occurred

        """
        self.duration = max(self.beats) - min(self.beats)
        logging.info('Successfully identified duration.')
        if self.duration < 5:
            logging.warning('Warning: Less than 5 seconds of ECG data being '
                            'used. Mean heart rate may be inaccurate.')
        return self.duration

    def get_mean_hr(self):
        """
        Mean heart rate is calculated as the number of beats detected
        divided by the duration.

        Returns:
            mean_hr: the calculated mean heart rate

        """
        self.mean_hr = self.num_beats/self.duration*60
        logging.info('Successfully identified mean heart rate.')
        if self.mean_hr < 40:
            logging.warning('Warning: Heart rate abnormally low. (<40 bmp)')
        if self.mean_hr > 180:
            logging.warning('Warning: Heart rate abnormally high. (>180 bmp)')
        return self.mean_hr

    def get_results(self):
        """
        Since beats are being measured peak-to-peak, the final peak
        detected notes the end of the final beat used to calculate
        mean heart rate and therefore is not recorded as a beat time

        Returns:
            metrics: dictionary containing mean heart rate, minimum and maximum
                    voltage, duration, number of beats, and times beats

        """
        metrics = {'Mean heart rate': '%.3f bpm' % round(self.mean_hr, 3),
                   'Minimum voltage': '%.3f V' % self.min_vol,
                   'Maximum voltage': '%.3f V' % self.max_vol,
                   'Duration': '%.3f s' % self.duration,
                   'Number of beats': '%.0f beats' % self.num_beats,
                   'Beat occurrence times (in seconds)': self.beats[
                                                         0:len(self.beats)-1],
                   }
        return metrics
