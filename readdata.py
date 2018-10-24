import numpy as np
import sys
import csv


def can_float(value):
    """This function takes in a string a determines whether or not it
    can be converted to a float.

    Args:
        value: the string to check if can be converted to float

    Returns:
        bool: True if can convert to float, False otherwise

    """
    try:
        float(value)
        return True
    except ValueError:
        print('Non-float value found in dataset.  Skipping this time, voltage pair')
        return False


def get_data(filename_arg):
        """This function opens the data file of interest and pulls time and voltage
        values from the data file to be used for calculating the heart rate.

        Args:
            filename_arg: name of test data file to be tested

        Returns:
            time: list containing the time values of the data set
            voltage: list containing the voltage values of the data set

        """
#        data_table = []
        time = []
        voltage = []
        try:
            #data_table = np.loadtxt(filename_arg, delimiter=",")
            #data_table = csv.reader(filename_arg, delimiter=',')
            open(filename_arg, 'r')

        except IOError:
            print("That file could not be found.  Please try again")
            sys.exit()

        data_table = np.loadtxt(filename_arg, delimiter=',')
        #data_table = csv.reader(filename_arg, delimiter=',')

        for index in data_table:
            if can_float(index[0]) and can_float(index[1]):
                time.append(float(index[0]))
                voltage.append(float(index[1]))
        return time, voltage
