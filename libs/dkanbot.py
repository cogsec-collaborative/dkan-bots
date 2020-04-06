import os
import requests
import json
import validators
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
def add_resource_to_dataset(ia_uri, trigger_source, dataset_nid=1):
    if uri:

        api = DatasetAPI(uri, user, password, False)
        # take the back-end of the IA uri so we don't have to import it separately
        source_uri = ia_uri[43:]
        if (validators.url(source_uri) == True):
            data = {
                'title': '[dkanbot] Link to ' + source_uri,
                'type': 'resource',
                'body' : {
                    'und': {
                        '0': {
                            'value': 'Data added by dkanbot from ' + str(trigger_source),
                        }
                    }
                },
                'field_dataset_ref': {
                    'und': {
                        '0': {
                            'target_id': dataset_nid,
                        }
                    }
                },
                'field_link_api': {
                    'und': {
                        '0': {
                            'url': ia_uri
                        }
                    }
                }
            }

            r = api.node('create', data=data)
            return json.loads(r.text)
        else:
            print("invalid source URI")
            return 1
