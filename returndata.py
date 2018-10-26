import json
import logging


def return_data(filename, metrics):
    """
    Creates JSON file containing metrics dictionary values for data set

    Args:
        filename: name of analyzed datafile that will be used for JSON
                file name
        metrics: dictionary containing values of interest obtained from
                the dataset

    Returns:

    """
    return_fname = filename.replace('.csv', '.json')
    return_file = open(return_fname, 'w')
    json.dump(metrics, return_file, indent=2)
    return_file.close()
    logging.info('Processing complete for file: %s. JSON file has been created'
                 ' containing values of interest.' % filename)
