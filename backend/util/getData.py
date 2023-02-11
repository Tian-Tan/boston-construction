import requests

def get_data(offset):
    ''' creates a json file that stores the data we get from the api, starting from the specified offset, with a limit of 100 data objects
    '''
    response = requests.get(f'https://data.boston.gov/api/3/action/datastore_search?offset={offset}&resource_id=36fcf981-e414-4891-93ea-f5905cec46fc').text
    f = open(f"../data/data-from-offset-{offset}.json", "w")
    f.write(response)
    f.close()

# Since the api limits calls to 100 data objects per call, we have to first see how many objects (ongoing construction) are there,
# and then call the api using offset 0, 100, 200, etc
get_data('0')       