from processdata import ProcessData
import returndata


def main():
    """
    Ask user for a data file number (x for test_data/test_datax.csv), calls to
    open file, process data, and return data in JSON file.

    Returns:

    Raises:
        IOError: if file cannot be opened, will ask user to input a
                new file number and try again

    """
    num = input('Enter test data file number')
    filename = ('test_data/test_data' + num + '.csv')
    ecg_series = None
    while ecg_series is None:
        try:
            ecg_series = ProcessData(filename)
        except IOError:
            num = input('Error, file not opened.  Please enter a new file '
                        'number.')
            filename = ('test_data/test_data' + num + '.csv')
    ecg_series.check_neg()
    ecg_series.handle_neg()
    ecg_series.get_time()
    ecg_series.get_voltage()
    ecg_series.get_min()
    ecg_series.get_max()
    ecg_series.get_peaks()
    ecg_series.get_num_beats()
    ecg_series.get_beats_time()
    ecg_series.get_peak_voltage()
    ecg_series.get_duration()
    ecg_series.get_mean_hr()
    results = ecg_series.get_results()
    returndata.return_data(filename, results)
    print('Completed.  Open %s to see results' % filename)


if __name__ == "__main__":
    main()
