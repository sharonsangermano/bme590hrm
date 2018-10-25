from processdata import ProcessData
import returndata


def main():
    num = input('Enter test data file number')
    filename = ('test_data/test_data' + num + '.csv')
    ecg_series = ProcessData(filename)
    ecg_series.check_data()
    print(len(ecg_series.get_time()))
    print(len(ecg_series.get_voltage()))
    print('The minimum voltage is', ecg_series.get_min(), 'V')
    print('The maximum voltage is', ecg_series.get_max(), 'V')
    print(ecg_series.get_peaks())
    print(ecg_series.get_num_beats())
    print(ecg_series.get_beats_time())
    print(ecg_series.get_peak_voltage())
    print('The duration is %.3f s' % ecg_series.get_duration())
    print('The mean heart rate is %.3f bpm' % ecg_series.get_mean_hr())
    results = ecg_series.get_results()
    returndata.return_data(filename, results)


if __name__ == "__main__":
    main()
