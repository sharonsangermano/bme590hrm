import csv
import logging
import math


def can_float(value):
    """Takes in a string a determines whether or not it
    can be converted to a float.

    Args:
        value: the string to check if can be converted to float

    Returns:
        bool: True if can convert to float, False otherwise

    Raises:
        ValueError: if value cannot be converted to float

    """
    try:
        float(value)
        return True
    except ValueError:
        logging.warning('Warning: Non-float value found in dataset.  Skipping '
                        'this time, voltage pair')
        return False


def get_data(filename_arg):
        """Open the data file of interest and pulls time and voltage values
        from the data file to be used for calculating the heart rate.

        Args:
            filename_arg: name of test data file to be tested

        Returns:
            time: list containing the time values of the data set (all floats)
            voltage: list containing the voltage values of the data
                    set (all floats)

        Raises:
            IOError: if file associated with filename_arg cannot be opened

        """
        time = []
        voltage = []
        try:
            open(filename_arg, 'r')
            logging.info('Successfully opened file: %s ' % filename_arg)

        except IOError as inst:
            logging.error('Error: File could not be opened. Please try again')
            raise inst

        data_file = open(filename_arg, 'r')

        data_table = csv.reader(data_file, delimiter=',')
        for index in data_table:
            if can_float(index[0]) and can_float(index[1]):
                if math.isnan(float(index[0])) or math.isnan(float(index[1])):
                    logging.warning('Warning: Null value found in dataset.  '
                                    'Skipping this time, voltage pair')
                else:
                    time.append(float(index[0]))
                    voltage.append(float(index[1]))
        return time, voltage
