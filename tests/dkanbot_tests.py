import unittest
from libs import dkanbot

class TestDKANBot(unittest.TestCase):
    # test internet archive submit
    def test_archive_submit(self):
        test_uri = 'https://www.example.com'
        result = dkanbot.upload_to_archive(test_uri)
        self.assertRegex(result, 'https:\/\/web\.archive\.org\/web\/[\d]+\/https:\/\/www\.example\.com$')

    # test get node_id
    def test_node_id(self):
        pass

    # test posting a resource to a dataset
    def test_resource_attach(self):
        pass

if __name__ == '__main__':
    unittest.main()
