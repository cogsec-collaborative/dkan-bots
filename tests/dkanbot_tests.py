import unittest
from libs import dkanbot
from dkan.client import DatasetAPI

class TestDKANBot(unittest.TestCase):

    # set up a dummy resource
    def setUp(self):
        uri = os.environ.get('DKAN_URI', False)
        user = os.environ.get('DKAN_USER', 'admin')
        password = os.environ.get('DKAN_PASSWORD', 'admin')

        if uri:
            api = DatasetAPI(uri, user, password)

            data = {
                'title': 'Test Suite Dataset',
                'type': 'dataset'
            }
            dataset = api.node('create', data=data)
            result = 

    # test internet archive submit
    def test_archive_submit(self):
        test_uri = 'https://www.example.com'
        result = dkanbot.upload_to_archive(test_uri)
        self.assertRegex(result, 'https:\/\/web\.archive\.org\/web\/[\d]+\/https:\/\/www\.example\.com$')

    # test get node_id
    def test_node_id(self):
        test_nid = '1'
        result = dkanbot.get_nodeid('Example dataset')
        self.assertEqual(test_nid, result)

    # test posting a resource to a dataset
    def test_resource_attach(self):
        # get a uri from IA
        uri_stub = 'https://www.example.com'
        test_uri = dkanbot.upload_to_archive(uri_stub)
        test_nid = '1'
        test_trigger = 'dkanbot unit test'
        # test posting it
        result = dkanbot.add_resource_to_dataset(test_uri, test_trigger, test_nid)
        # first, make sure it's not an error return
        self.assertNotEqual(result, 1)
        # now, make sure it matches the node_id we got back
        self.assertEqual(dkanbot.get_nodeid('[dkanbot] Link to ' + uri_stub, result['nid'])


if __name__ == '__main__':
    unittest.main()
