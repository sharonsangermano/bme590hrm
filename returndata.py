import json
import logging


def return_data(filename, results):
    return_fname = filename.replace('.csv', '.json')
    return_file = open(return_fname, 'w')
    json.dump(results, return_file)
    return_file.close()
    logging.info('Processing complete for file: %s. JSON file has been created'
                 ' containing values of interest.' % filename)
