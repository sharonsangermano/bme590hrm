from processdata import ProcessData
import readdata

time, voltage = readdata.get_data('test_data/test_data1.csv')
x = ProcessData(time, voltage)


def test_get_time():
    t_get = x.get_time()
    assert t_get == [0.04, 0.12, 0.3]


def test_get_voltage():
    t_vol = x.get_voltage()
    assert t_vol == [0.2, 0.3, 0.4]


def test_get_min():
    min_vol = x.get_min()
    assert min_vol == 0.2


def test_get_max():
    max_vol = x.get_max()
    assert max_vol == 0.4


def test_get_peaks():
    peaks = x.get_peaks()
    assert peaks == [77, 370, 663, 947, 1231, 1515, 1809, 2045, 2403, 2706, 2998, 3283, 3560, 3863, 4171,
                     4466, 4765, 5061, 5347, 5634, 5918, 6215, 6527, 6824, 7106, 7393, 7670, 7953, 8246,
                     8539, 8837, 9142, 9432, 9710]


def test_get_num_beats():
    x.get_peaks()
    num_beats = x.get_num_beats()
    assert num_beats == 34


def test_get_beats_time():
    x.get_peaks()
    beat_times = x.get_beats_time()
    assert beat_times == [0.214, 1.028, 1.842, 2.631, 3.419, 4.208, 5.025, 5.681, 6.675, 7.517, 8.328,
                          9.119, 9.889, 10.731, 11.586, 12.406, 13.236, 14.058, 14.853, 15.65, 16.439,
                          17.264, 18.131, 18.956, 19.739, 20.536, 21.306, 22.092, 22.906, 23.719, 24.547,
                          25.394, 26.2, 26.972]


def test_get_peak_voltage():
    x.get_peaks()
    peak_volts = x.get_peak_voltage()
    assert peak_volts == [0.84, 0.94, 0.96, 0.86, 0.82, 0.885, 0.945, 0.875, 0.885, 0.89, 0.925, 0.865,
                          0.835, 0.935, 0.89, 0.795, 0.85, 0.905, 0.825, 0.97, 0.895, 0.975, 0.875, 0.88,
                          0.935, 1.05, 0.88, 0.92, 0.955, 0.845, 0.725, 0.83, 1.045, 0.855]


def test_get_duration():
    x.get_peaks()
    x.get_beats_time()
    dur = round(x.get_duration(), 3)
    assert dur == 26.758


def test_get_mean_hr():
    x.get_peaks()
    x.get_beats_time()
    x.get_duration()
    x.get_num_beats()
    mhr = round(x.get_mean_hr(), 3)
    assert mhr == 76.239
