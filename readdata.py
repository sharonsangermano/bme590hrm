import numpy as np
import sys
import csv
import logging
import math


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
        logging.warning('Warning: Non-float value found in dataset.  Skipping '
                        'this time, voltage pair')
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
        time = []
        voltage = []
        try:
            open(filename_arg, 'r')
            logging.info('Successfully opened file: %s ' % filename_arg)

        except IOError:
            logging.error('Error: File could not be found. Please try again')
            sys.exit()

        data_file = open(filename_arg, 'r')

        data_table = csv.reader(data_file, delimiter=',')
        # data_table = csv.reader(data_file)
        for index in data_table:
            # if index[0] is None or index[1] is None:
            #    data_table.pop(index)
            #    print("Missing datapoint, skipping this time, voltage pair")
            if can_float(index[0]) and can_float(index[1]):
                if math.isnan(float(index[0])) or math.isnan(float(index[1])):
                    logging.warning('Warning: Null value found in dataset.  '
                                    'Skipping this time, voltage pair')
                else:
                    time.append(float(index[0]))
                    voltage.append(float(index[1]))
        return time, voltage
