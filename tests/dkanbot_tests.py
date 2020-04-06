import unittest
import json
from libs import dkanbot
from dkan.client import DatasetAPI

class TestDKANBot(unittest.TestCase):
    # set up a dummy resource
    def setUp(self):
        self.api = dkanbot.create_api_session()
        data = {
            'title': 'Test Suite Dataset',
            'type': 'dataset'
        }
        dataset = self.api.node('create', data=data)
        result = dataset.json()
        self.dataset_nid = result['nid']
        self.dataset_uri = result['uri']
        self.test_uri = 'https://www.example.com'
        self.trigger = "Dkanbot unit test suite"
        self.cleanup = [self.dataset_nid]

    # clean up
    def tearDown(self):
        self.cleanup = list(set(self.cleanup))
        for node in self.cleanup:
            delete = self.api.node('delete', node_id=node)
            self.assertEqual(delete.status_code, 200)
        self.cleanup = []

    # test internet archive submit
    def test_archive_submit(self):
        result = dkanbot.upload_to_archive(self.test_uri)
        self.assertRegex(result, 'https:\/\/web\.archive\.org\/web\/[\d]+\/https:\/\/www\.example\.com$')

    # test get node_id
    def test_dataset_node_id(self):
        result = dkanbot.get_dataset_nodeid('Test Suite Dataset')
        self.assertEqual(self.dataset_nid, result)

    # test posting a resource to a dataset
    def test_resource_attach(self):
        ia_uri = dkanbot.upload_to_archive(self.test_uri)
        # test posting it
        result = dkanbot.add_resource_to_dataset(ia_uri, self.trigger, self.dataset_nid)
        self.cleanup.append(result['nid'])
        # first, make sure it's not an error return
        self.assertNotEqual(result, 1)
        # now, make sure it matches the node_id we got back
        self.assertEqual(dkanbot.get_resource_nodeid('[dkanbot] Link to ' + self.test_uri), result['nid'])
        # now, make sure the URL matches
        r = self.api.node('retrieve', node_id=result['nid'])
        retrieved = r.json()
        self.assertEqual(retrieved['field_link_api']['und'][0]['url'], ia_uri)

if __name__ == "__main__":
    unittest.main()
