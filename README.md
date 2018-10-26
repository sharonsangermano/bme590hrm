# bme590hrm
Heart Rate Monitor Assignment 

## Code
**main.py:** Asks user for test data file number (x for test_data/test_datax.csv), checks if 
    file exists and prompts user for a new file number if does not exist.  Calls functions to 
    read, process, and return data.
    
**readdata.py:** Reads in data from test file to create time and voltage lists.  Eliminates 
    all time-voltage pairs containing a non-float or NULL value.  
    
**test_readdata.py:** Tests *readdata.py* functions. 

**processdata.py:** Creates the ProcessData class containing functions to obtained the wanted
    information from the data.  Voltage peaks are detected using a moving average algorithm.  
    A heart beat is considered the time from one peak voltage to the next peak.  The duration is 
    measured as the time from the first peak voltage to the last peak voltage detected.  The 
    number of beats detected is one fewer than the number of peaks detected (peak to peak = one 
    beat). Additional methods detect and handle data sets with all negative voltages and inverted 
    signals. Dictionary is created to return metrics. 
    
**test_processdata.py:** Tests *processdata.py* functions. 

**returndata.py:** Receives metrics dictionary and creates a JSON file (with the same name
    and location as the .csv data file of interest) to display the metrics.
    
**test_returndata.py:** Tests *returndata.py* functions

**hrm_log.txt:** Logs errors, warnings, and important info as data is being processed. File 
    is cleared at the start of each run so only contains information from the most recent 
    execution of the code.
    
**test_data:** time - voltage ECG data sets, location of JSON output files 

**Other test files:** files used to test specific functions

##
[![Build Status](https://travis-ci.org/sharonsangermano/bme590hrm.svg?branch=master)](https://travis-ci.org/sharonsangermano/bme590hrm)