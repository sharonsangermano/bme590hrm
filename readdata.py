import numpy as np
import sys
import csv


def can_float(value):
    try:
        float(value)
        return True
    except ValueError:
        print('Non-float value found in dataset.  Skipping this time, voltage pair')
        return False


def get_data(filename_arg):
        """
            Args:
            Attributes:
            Returns:
                data_table (list???):
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
