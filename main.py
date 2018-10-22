from readdata import ReadData
from processdata import ProcessData


def main():
    current_data = ReadData('test_data/test_data1.csv')
    full_data = current_data.get_data()
    time_data = current_data.get_time()
    voltage_data = current_data.get_voltage()
    ecg_series = ProcessData(full_data, time_data, voltage_data)
    print(full_data)
    print(time_data)
    print(ecg_series.get_time())
    print(ecg_series.get_voltage())
    print(voltage_data)
    print(ecg_series.get_min())
    print(ecg_series.get_max())
    print(ecg_series.get_duration())
    print(ecg_series.get_peaks())
    print(ecg_series.get_num_beats())
    print(ecg_series.get_beats_time())
    print(ecg_series.get_peak_voltage())


if __name__ == "__main__":
    main()