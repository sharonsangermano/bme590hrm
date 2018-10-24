import readdata
from processdata import ProcessData


def main():
    num = input('Enter test data file number')
    ecg_series = ProcessData('test_data/test_data' + num + '.csv')
    print(ecg_series.get_time())
    print(ecg_series.get_voltage())
    print('The minimum voltage is', ecg_series.get_min(), 'V')
    print('The maximum voltage is', ecg_series.get_max(), 'V')
    print(ecg_series.get_peaks())
    print(ecg_series.get_num_beats())
    print(ecg_series.get_beats_time())
    print(ecg_series.get_peak_voltage())
    print('The duration is %.3f s' % ecg_series.get_duration())
    print('The mean heart rate is %.3f bpm' % ecg_series.get_mean_hr())


if __name__ == "__main__":
    main()
