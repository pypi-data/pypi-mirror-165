import unittest
import os


class CompVisTestCase(unittest.TestCase):
    
    def test_manual_rps_presence(self):
        manual_game_script = 'manual_rps.py'
        self.assertIn(manual_game_script, os.listdir('.'), 'There is no manual_rps.py file in your project folder. If it is there, make sure it is named correctly, and that it is in the main folder')
        # with open('manual_rps.py', 'r') as f:
        #     manual_game_code = f.read()
        # possible_if_main = ['if __name__ == "__main__":',
        #                     'if __name__ == "__main__" :',
        #                     'if __name__=="__main__":',
        #                     'if __name__ =="__main__":',
        #                     'if __name__== "__main__":',
        #                     'if __name__=="__main__" :',
        #                     'if __name__ =="__main__" :',
        #                     'if __name__== "__main__" :',
        #                     "if __name__ == '__main__':",
        #                     "if __name__ == '__main__' :",
        #                     "if __name__=='__main__':",
        #                     "if __name__ =='__main__':",
        #                     "if __name__== '__main__':",
        #                     "if __name__=='__main__' :",
        #                     "if __name__ =='__main__' :",
        #                     "if __name__== '__main__' :",
        # ]
        # if True in (x in manual_game_code for x in possible_if_main):
        #     if_main = True
        # else:
        #     if_main = False
        # self.assertTrue(if_main, 'You should have a if __name__ == "__main__" statement in your manual_rps.py file')


if __name__ == '__main__':

    unittest.main(verbosity=2)
    