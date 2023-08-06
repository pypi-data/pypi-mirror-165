import unittest
import camera_rps
from inspect import getsource

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

if __name__ == '__main__':

    unittest.main(verbosity=2)
    