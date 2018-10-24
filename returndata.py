import json


def return_data(filename, results):
    return_fname = filename.replace('.csv', '.json')
    return_file = open(return_fname, 'w')
    json.dump(results, return_file)
    return_file.close()
