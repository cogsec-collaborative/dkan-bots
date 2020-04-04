
import requests
import json
from dkan.client import DatasetAPI

# set these as environment variables for now
# TODO add a config file template
uri = os.environ.get('DKAN_URI', False)
user = os.environ.get('DKAN_USER', 'admin')
password = os.environ.get('DKAN_PASSWORD', 'admin')

api = DatasetAPI(uri, user, password)

# toss url into internet archive
def upload_to_archive(target_url):
    # get everything set up
    session = requests.Session()
    ia_url  = 'https://web.archive.org/save/' + target_url
    headers = {"Accept": "application/json, text/plain, */*", "user-agent": "dkanbot/0.1" }

    # make the actual request
    response = session.get(ia_url, headers=headers)

    # return the asset url
    asset_url = 'https://web.archive.org' + reponse.headers['Content-Location']
    return asset_url

# call DKAN to get the node id from the list of datasets
def get_nodeid(title, api):
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
# take our url and specified dataset
