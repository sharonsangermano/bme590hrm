import json


def test_return_data():
    from returndata import return_data
    test_filename = 'testing_return_data.csv'
    test_results = {'Test item 1': 37,
                    'Test item 2': [1, 2, 3],
                    'Test item 3': 'This works!',
                    }
    return_data(test_filename, test_results)
    check_output = json.load(open(test_filename.replace('.csv', '.json')))
    assert check_output == test_results
