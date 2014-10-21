from pytagcloud import create_tag_image, create_html_data, make_tags, \
    LAYOUT_HORIZONTAL, LAYOUTS
from pytagcloud.colors import COLOR_SCHEMES
from pytagcloud.lang.counter import get_tag_counts
from string import Template
import os
import time
import unittest

class Test(unittest.TestCase):
    """
    Generate tag clouds and save them to <YOURHOME>/pytagclouds/
    Note: All tests are disabled ('_' prefixed) by default
    """
    
    def setUp(self):
        self.test_output = os.path.join(os.getcwd(), 'out')
        self.hound = open(os.path.join(os.getcwd(), 'pg2852.txt'), 'r')
        
        if not os.path.exists(self.test_output):
            os.mkdir(self.test_output )            
            
    def tearDown(self):
        self.hound.close()
        
        
    def test_large_tag_image(self):
        start = time.time()
        tags = make_tags(get_tag_counts(self.hound.read())[:80], maxsize=120, 
                         colors=COLOR_SCHEMES['audacity'])
        create_tag_image(tags, os.path.join(self.test_output, 'cloud_large.png'), 
                         size=(900, 600), background=(0, 0, 0, 255), 
                         layout=LAYOUT_HORIZONTAL, fontname='Lobster')
        print("Duration: %d sec" % (time.time() - start))
    

if __name__ == "__main__":
    unittest.main()