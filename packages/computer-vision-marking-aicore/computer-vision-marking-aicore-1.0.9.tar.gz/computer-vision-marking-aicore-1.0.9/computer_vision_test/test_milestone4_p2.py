import unittest
import camera_rps
from inspect import getsource
import os
import spacy
from urllib.request import urlopen
class CompVisTestCase(unittest.TestCase):
    
    def test_prediction_presence(self):
        self.assertIn("get_prediction", camera_rps.__dict__, "You should have a function called get_prediction in your camera_rps.py file")
        func = getsource(camera_rps.get_prediction)
        self.assertIn("return", func, "The function get_prediction should 'return' a prediction")
    
    def test_time_presence(self):
        with open('camera_rps.py', 'r') as f:
            camera_script = f.read()
        self.assertIn("time", camera_script, "You should call the function time() to create a countdown")

    def test_number_wins(self):
        with open('camera_rps.py', 'r') as f:
            camera_script = f.read()
        comp_wins_possibilities = ["computer_wins == 3",
                                   "computer_wins==3",
                                   "computer_wins== 3",
                                   "computer_wins ==3",
                                   "computer_wins >= 3",
                                   "computer_wins>=3",
                                   "computer_wins>= 3",
                                   "computer_wins >=3",
                                   "computer_wins > 2",
                                   "computer_wins>2",
                                   "computer_wins >2",
                                   "computer_wins> 2",
        ]
        user_wins_possibilities = ["user_wins == 3",
                                   "user_wins==3",
                                   "user_wins== 3",
                                   "user_wins ==3",
                                   "user_wins >= 3",
                                   "user_wins>=3",
                                   "user_wins>= 3",
                                   "user_wins >=3",
                                   "user_wins > 2",
                                   "user_wins>2",
                                   "user_wins >2",
                                   "user_wins> 2",
        ]
        rounds_played_possibilities = ["rounds_played == 5",
                                       "rounds_played==5",
                                       "rounds_played== 5",
                                       "rounds_played ==5",
                                       "rounds_played >= 5",
                                       "rounds_played>=5",
                                       "rounds_played>= 5",
                                       "rounds_played >=5",
                                       "rounds_played > 4",
                                       "rounds_played>4",
                                       "rounds_played >4",
                                       "rounds_played> 4",
        ]
        if True in (x in camera_script for x in comp_wins_possibilities):
            comp_wins = True
        else:
            comp_wins = False
        if True in (x in camera_script for x in user_wins_possibilities):
            user_wins = True
        else:
            user_wins = False
        if True in (x in camera_script for x in rounds_played_possibilities):
            rounds_played = True
        else:
            rounds_played = False
        cond = (comp_wins and user_wins) or rounds_played
        self.assertTrue(cond, "You should have a condition that checks if the computer or user wins or if the game is over. It can be either comparing both computer_wins and user_wins reached 3 or checking that rounds_played is 5")

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
    