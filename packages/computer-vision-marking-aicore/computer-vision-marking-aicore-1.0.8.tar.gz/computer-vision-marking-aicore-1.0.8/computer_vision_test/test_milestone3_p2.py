import unittest
import os
import manual_rps
from inspect import getsource

class CompVisTestCase(unittest.TestCase):
    
    def test_computer_choice_presence(self):
        self.assertIn("get_computer_choice", manual_rps.__dict__, "You should have a function called get_computer_choice in your manual_rps.py file")
    
    def test_user_choice(self):
        self.assertIn("get_user_choice", manual_rps.__dict__, "You should have a function called get_user_choice in your manual_rps.py file")
        self.assertIn("input", getsource(manual_rps.get_user_choice), "The function get_user_choice is not asking for user input")
        self.assertIn("while", getsource(manual_rps.get_user_choice), "The function get_user_choice needs to iteratively ask the user for input until they enter a valid choice. Use a while loop to do so")
    
    def test_get_winner(self):
        self.assertIn("get_winner", manual_rps.__dict__, "You should have a function called get_winner in your manual_rps.py file")
        args = getsource(manual_rps.get_winner).split('get_winner(')[1].split(')')[0].split(',')
        self.assertEqual(len(args), 2, "The function get_winner should take exactly two arguments: computer_choice and user_choice")        
        func = getsource(manual_rps.get_winner)
        self.assertIn("if", func, "The function get_winner should have some logic in it, I can't see any if statements")
        self.assertIn("elif", func, "The function get_winner should have some logic in it, I can't see any elif statements")
        self.assertIn("else", func, "The function get_winner should have some logic in it, I can't see any else statements. Even though it's not strictly necessary, implement it on your code")
    
    def test_play(self):
        self.assertIn("play", manual_rps.__dict__, "You should have a function called play in your manual_rps.py file")
        func = getsource(manual_rps.play)
        self.assertIn("get_computer_choice", func, "The function play should call get_computer_choice")
        self.assertIn("get_user_choice", func, "The function play should call get_user_choice")
        self.assertIn("get_winner", func, "The function play should call get_winner")


if __name__ == '__main__':

    unittest.main(verbosity=2)
    