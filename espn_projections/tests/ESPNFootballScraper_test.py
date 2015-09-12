import logging
from ESPNFootballScraper import ESPNFootballScraper
import sys
import unittest

class ESPNFootballScraper_test(unittest.TestCase):

    def setUp(self):
        self.efs = ESPNFootballScraper()
        self.urls = {
            '0': '',
            '40': ''
        }

    def test_params(self):
        log= logging.getLogger(__file__)
        log.debug('testing params')
        self.assertEqual(self.efs.maxindex, 400, msg='maxindex should be {0}'.format(self.efs.maxindex))
        
if __name__=='__main__':
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger(__file__).setLevel(logging.DEBUG)
    unittest.main()
