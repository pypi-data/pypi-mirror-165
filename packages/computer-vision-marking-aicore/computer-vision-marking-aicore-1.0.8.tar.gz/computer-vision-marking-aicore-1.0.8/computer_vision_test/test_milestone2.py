import unittest
import os
import importlib.util


class CompVisTestCase(unittest.TestCase):
    
    def test_requirements_presence(self):
        model_path = 'requirements.txt'
        self.assertIn(model_path, os.listdir('.'), 'There is no requirements.txt file in your project folder')
        with open('requirements.txt') as f:
            requirements = f.read().splitlines()
        libraries = [r.split()[0] for r in requirements[2:]]
        self.assertIn('ipykernel', libraries, 'You should have ipykernel in your requirements.txt file')
        self.assertIn('ipython', libraries, 'You should have ipython in your requirements.txt file')
        self.assertGreater(len(requirements), 10, 'You should have at least 10 lines in your requirements.txt file')

    def test_can_import_opencv(self):
        cv_package = importlib.util.find_spec('cv2')
        self.assertIsNotNone(cv_package, 'You should have OpenCV in your requirements.txt file. If it is not installed, you can install it with pip install opencv-python')

    def test_can_import_numpy(self):
        np_package = importlib.util.find_spec('numpy')
        self.assertIsNotNone(np_package, 'You should have numpy in your requirements.txt file. It is installed when you install tensorflow, so make sure you have tensorflow installed as well')

    def test_can_import_keras(self):
        keras_package = importlib.util.find_spec('keras')
        self.assertIsNotNone(keras_package, 'You should have keras in your requirements.txt file. It is installed when you install tensorflow, so make sure you have tensorflow installed as well')
    
if __name__ == '__main__':

    unittest.main(verbosity=2)
    