import os
import requests
import json
from dkan.client import DatasetAPI

# set these as environment variables for now
# TODO add a config file template
uri = os.environ.get('DKAN_URI', False)
user = os.environ.get('DKAN_USER', 'admin')
password = os.environ.get('DKAN_PASSWORD', 'admin')

# toss url into internet archive
def upload_to_archive(source_url):
    # get everything set up
    session = requests.Session()
    ia_url  = 'https://web.archive.org/save/' + source_url
    headers = {"Accept": "application/json, text/plain, */*", "user-agent": "dkanbot/0.1" }

    # make the actual request
    response = session.get(ia_url, headers=headers)

    # return the asset url
    asset_url = 'https://web.archive.org' + response.headers['Content-Location']
    return asset_url

# call DKAN to get the node id from the list of datasets
def get_nodeid(title):
    if uri:
        api = DatasetAPI(uri, user, password)

    # set up the query params
    params = {
        'parameters[type]'  : 'dataset',
        'parameters[title]' : title
    }
    # make the api request and turn it into something usable
    r = api.node(params=params)
    result = json.loads(r.content)

    # if the results aren't bonkers, return them
    assert (len(result) == 1)
    return result[0]['nid']

# add internet archive url to defined dkan dataset
def add_resource_to_dataset(url, nid, dataset="Miscellaneous Covid-19"):
    # if uri:
    #   api = DatasetAPI(uri, user, password, True)
    #
    #   payload = {
    #     'parameters[type]': 'resource',
    #     'parameters[title]': 'REPLACE',
    #
    #     }
    #
    #   Attach the file to the resource node
    #   r = api.attach_file_to_node(csv, resource['nid'], 'field_upload')
    #   print(r.status_code)
    #   print(r. text)
    #   resource = api.node('retrieve', node_id=resource['nid'])
    #   print(resource.json()['field_upload'])
    pass
