from hangman.hangman_solution import Hangman
from hangman.hangman_solution import play_game
import unittest
from contextlib import redirect_stdout
import io
from unittest.mock import patch, call

class HangmanTestCase(unittest.TestCase):

    def setUp(self):
        word_list = ['WatermelonBanana']
        f = io.StringIO()
        with redirect_stdout(f):
            self.game = Hangman(word_list, 5)
        self.init_message = f.getvalue()
    
    def test_word(self):
        self.assertEqual(self.game.word, 'WatermelonBanana', 'The word attribute is not properly set')
        self.assertEqual(self.game.num_letters, len(set(self.game.word)), 'The num_letters attribute is not properly set')
    
    def test_word_guessed(self):
        self.assertEqual(self.game.word_guessed, ['_'] * len(self.game.word), 'The word_guessed attribute is not properly set')
        
    def test_num_lives_exists(self):
        self.assertTrue(hasattr(self.game, 'num_lives'), 'The num_lives attribute does not exist')

    def test_num_lives(self):
        self.assertEqual(self.game.num_lives, 5, 'The num_lives attribute is not properly set')

    @patch('builtins.input', side_effect=['aaa'])
    def test_check_invalid_input(self, input_mock):
        self.assertIn('ask_letter', Hangman.__dict__.keys(), 'The ask_letter method does not exist, did you remove it?')
        f = io.StringIO()
        with redirect_stdout(f):
            with self.assertRaises(Exception) as context:
      
                self.game.ask_letter()
            actual_value = f.getvalue()
        expected = 'Please, enter just one character\n'
        self.assertEqual(actual_value, expected, f'The ask_letter method is not checking for invalid inputs. If it does, make sure that the message has the right format. It should print "Please, enter just one character", but it is printing "{actual_value}" instead')

if __name__ == '__main__':

    unittest.main(verbosity=0)
    