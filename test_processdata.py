from processdata import ProcessData
import pytest
import logging


def test_init():
    test_obj = ProcessData('test_get.csv')
    assert test_obj.file_name == 'test_get.csv'
    assert test_obj.time == [0.04, 0.12, 0.3]
    assert test_obj.voltage == [0.2, 0.3, 0.4]
    assert test_obj.num_beats == 0
    assert test_obj.peaks == []
    assert test_obj.beats == []
    assert test_obj.volts == []
    assert test_obj.duration == 0
    assert test_obj.mean_hr == 0
    assert test_obj.min_vol == 0
    assert test_obj.max_vol == 0
    assert 'Successfully imported data from:' in open('hrm_log.txt').read()


def test_init_fail():
    with pytest.raises(IOError):
        ProcessData('fake_file.csv')


@pytest.fixture
def test_load():
    return ProcessData('test_data/test_data1.csv')


def test_get_time(test_load):
    t_get = test_load.get_time()
    assert t_get[0:10] == [0, 0.003, 0.006, 0.008, 0.011, 0.014, 0.017, 0.019,
                           0.022, 0.025]


def test_get_voltage(test_load):
    t_vol = test_load.get_voltage()
    assert t_vol[0:10] == [-0.145, -0.145, -0.145, -0.145, -0.145, -0.145,
                           -0.145, -0.145, -0.12, -0.135]


def test_get_min(test_load):
    min_vol = test_load.get_min()
    assert min_vol == -0.68


def test_get_max(test_load):
    max_vol = test_load.get_max()
    assert max_vol == 1.05


def test_get_peaks(test_load):
    peaks = test_load.get_peaks()
    assert peaks == [77, 370, 663, 947, 1231, 1515, 1809, 2045, 2403, 2706,
                     2998, 3283, 3560, 3863, 4171, 4466, 4765, 5061, 5347,
                     5634, 5918, 6215, 6527, 6824, 7106, 7393, 7670, 7953,
                     8246, 8539, 8837, 9142, 9432, 9710]


def test_get_num_beats(test_load):
    test_load.get_peaks()
    num_beats = test_load.get_num_beats()
    assert num_beats == 33


def test_get_beats_time(test_load):
    test_load.get_peaks()
    beat_times = test_load.get_beats_time()
    assert beat_times == [0.214, 1.028, 1.842, 2.631, 3.419, 4.208, 5.025,
                          5.681, 6.675, 7.517, 8.328, 9.119, 9.889, 10.731,
                          11.586, 12.406, 13.236, 14.058, 14.853, 15.65,
                          16.439, 17.264, 18.131, 18.956, 19.739, 20.536,
                          21.306, 22.092, 22.906, 23.719, 24.547, 25.394,
                          26.2, 26.972]


def test_get_peak_voltage(test_load):
    test_load.get_peaks()
    peak_volts = test_load.get_peak_voltage()
    assert peak_volts == [0.84, 0.94, 0.96, 0.86, 0.82, 0.885, 0.945, 0.875,
                          0.885, 0.89, 0.925, 0.865, 0.835, 0.935, 0.89, 0.795,
                          0.85, 0.905, 0.825, 0.97, 0.895, 0.975, 0.875, 0.88,
                          0.935, 1.05, 0.88, 0.92, 0.955, 0.845, 0.725, 0.83,
                          1.045, 0.855]


def test_get_duration(test_load):
    test_load.get_peaks()
    test_load.get_beats_time()
    dur = round(test_load.get_duration(), 3)
    assert dur == 26.758


def test_get_mean_hr(test_load):
    test_load.get_peaks()
    test_load.get_beats_time()
    test_load.get_duration()
    test_load.get_num_beats()
    mhr = round(test_load.get_mean_hr(), 3)
    assert mhr == 73.997


def test_get_results(test_load):
    test_load.get_peaks()
    test_load.get_min()
    test_load.get_max()
    beat_times = test_load.get_beats_time()
    test_load.get_duration()
    test_load.get_num_beats()
    test_load.get_mean_hr()
    return_dic = test_load.get_results()
    dic_results = {'Mean heart rate': '%.3f bpm' %
                                      round(test_load.get_mean_hr(), 3),
                   'Minimum voltage': '%.3f V' % test_load.get_min(),
                   'Maximum voltage': '%.3f V' % test_load.get_max(),
                   'Duration': '%.3f s' % test_load.get_duration(),
                   'Number of beats': '%.0f beats' % test_load.get_num_beats(),
                   'Beat occurrence times (in seconds)':
                       beat_times[0:len(beat_times) - 1],
                   }
    assert dic_results == return_dic


@pytest.mark.parametrize('file, is_neg', [
    (ProcessData('test_neg_data.csv'), False),
    (ProcessData('test_pos_data.csv'), True)
])
def test_check_neg(file, is_neg):
    neg_check = file.check_neg()
    assert neg_check == is_neg


def test_handle_neg():
    neg = ProcessData('test_neg_data.csv')
    neg.check_neg()
    vol = neg.handle_neg()
    assert vol == [1.25, 0.6, 1.15, 1.2, 1.05, 0.9, 0.7, 0.6, 1.4]
    assert 'Warning: No positive voltages detected. all voltage ' \
           'values shifted up 1.5V. Minimum and maximum voltage values ' \
           'may not be accurate' in open('hrm_log.txt').read()


def test_inv():
    test = ProcessData('test_invert.csv')
    peaks = test.get_peaks()
    assert peaks == [88, 441, 790]
    assert 'Warning: Inverted ECG signal detected peaks detected using ' \
           'inversion of input' in open('hrm_log.txt').read()


def test_num_beats_log():
    test = ProcessData('test_get.csv')
    test.peaks = [1, 2, 3]
    test.get_num_beats()
    assert 'Warning: Less than 5 beats detected. Mean ' \
           'heart rate may be inaccurate.' in open('hrm_log.txt').read()


def test_duration_log():
    test = ProcessData('test_get.csv')
    test.beats = [0.03, 4.5]
    test.get_duration()
    assert 'Warning: Less than 5 seconds of ECG data being used. Mean ' \
           'heart rate may be inaccurate.' in open('hrm_log.txt').read()


def test_high_mhr_log():
    test = ProcessData('test_get.csv')
    test.num_beats = 200
    test.duration = 60
    test.get_mean_hr()
    assert 'Warning: Heart rate abnormally high. (>180 bmp)' in \
           open('hrm_log.txt').read()


def test_low_mhr_log():
    test = ProcessData('test_get.csv')
    test.num_beats = 30
    test.duration = 60
    test.get_mean_hr()
    assert 'Warning: Heart rate abnormally low. (<40 bmp)' in \
           open('hrm_log.txt').read()
