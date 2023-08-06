import unittest
import os

class HangmanTestCase(unittest.TestCase):

    def test_presence(self):
        dir_list = os.listdir('hangman')
        self.assertIn('hangman_solution.py', dir_list, 'The hangman_solution.py file is not in the hangman directory')
    
    def test_diff(self):
        solution_path = 'hangman/hangman_solution.py'
        template_path = 'hangman/hangman_Template.py'
        with open(solution_path, 'r') as f:
            solution = f.read()
        with open(template_path, 'r') as f:
            template = f.read()
        self.assertNotEqual(solution, template, 'The hangman_solution.py file is identical to the hangman_Template.py file')
    
    def test_presence_ask_letter(self):
        solution_path = 'hangman/hangman_solution.py'
        with open(solution_path, 'r') as f:
            solution = f.read()
        self.assertIn('game.ask_letter()', solution.split('play_game(word_list)')[1], 'The ask_letter method is not called in the play_game function')
        


if __name__ == '__main__':

    unittest.main(verbosity=2)
    