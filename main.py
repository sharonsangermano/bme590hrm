from readdata import ReadData
from processdata import ProcessData


def main():
    current_data = ReadData('test_data/test_data1.csv')
    time, voltage = current_data.get_data()
    ecg_series = ProcessData(time, voltage)
    print(time)
    print(voltage)
    print(ecg_series.get_time())
    print(ecg_series.get_voltage())
    print('The minimum voltage is', ecg_series.get_min(), 'V')
    print('The maximum voltage is', ecg_series.get_max(), 'V')
    print('The duration is', ecg_series.get_duration(), 's')
    print(ecg_series.get_peaks())
    print(ecg_series.get_num_beats())
    print(ecg_series.get_beats_time())
    print(ecg_series.get_peak_voltage())
    print('The mean heart rate is %.3f bpm' % ecg_series.get_mean_hr())


if __name__ == "__main__":
    main()
