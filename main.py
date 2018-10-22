from readdata import ReadData
#from processdata import ProcessData


def main():
    current_data = ReadData('test_data/test_data1.csv')
    #processed_data = ProcessData(current_data)
    full_data = current_data.get_data()
    time_data = current_data.get_time()
    voltage_data = current_data.get_voltage()
    print(full_data)
    print(time_data)
    print(voltage_data)
    print(current_data.get_min())
    print(current_data.get_max())
    print(current_data.get_duration())
    #print(current_data.get_correlation())
    print(current_data.get_peaks())
    print(current_data.get_num_beats())
    print(current_data.get_beats_time())
    print(current_data.get_peak_voltage())


if __name__ == "__main__":
    main()