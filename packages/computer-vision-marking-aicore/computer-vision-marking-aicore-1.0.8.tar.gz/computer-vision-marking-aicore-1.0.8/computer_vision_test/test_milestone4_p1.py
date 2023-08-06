import unittest
import os
import spacy
from urllib.request import urlopen

class CompVisTestCase(unittest.TestCase):
    
    def test_camera_rps_presence(self):
        camera_game_script = 'camera_rps.py'
        self.assertIn(camera_game_script, os.listdir('.'), 'There is no camera_rps.py file in your project folder. If it is there, make sure it is named correctly, and that it is in the main folder')

    def test_presence_readme(self):
        self.assertIn('README.md', os.listdir('.'), 'You should have a README.md file in your project folder')
        with open('README.md', 'r') as f:
            readme = f.read()
        self.assertGreater(len(readme), 2000, 'The README.md file should be at least 2000 characters long')
        nlp = spacy.load("en_core_web_md")
        documentation = urlopen("https://aicore-files.s3.amazonaws.com/documentation.md")
        tdata = str(documentation.read(), 'utf-8')
        doc_1 = nlp(readme)
        doc_2 = nlp(tdata)
        self.assertLessEqual(doc_1.similarity(doc_2), 0.975, 'The README.md file is almost identical to the one provided in the template')
        number_hash = readme.count('#')
        self.assertGreaterEqual(number_hash, 3, 'The README.md file at least a subheading. Remember to use ## to create subheadings')
        image_html = "<img"
        image_md = "!["
        cond = (image_html in readme) or (image_md in readme)
        self.assertTrue(cond, 'You should have at least one image in your README.md file')

if __name__ == '__main__':

    unittest.main(verbosity=2)
    