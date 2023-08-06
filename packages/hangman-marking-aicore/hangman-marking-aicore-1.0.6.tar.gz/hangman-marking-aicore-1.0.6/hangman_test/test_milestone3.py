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
        self.initial_num_letters = self.game.num_letters

    @patch('builtins.input', side_effect=['aaa'])
    def test_check_invalid_input(self, input_mock):
        self.assertIn('ask_letter', Hangman.__dict__.keys(), 'The ask_letter method does not exist, did you remove it?')
        f = io.StringIO()
        with redirect_stdout(f):
            with self.assertRaises(Exception) as context:
                self.game.ask_letter()
            actual_value = f.getvalue()
        expected = 'Please, enter just one character\n'
        self.assertEqual(actual_value, expected, f'The ask_letter method is not checking for invalid inputs. If it does, make sure that the message has the right format. When you enter more than a character, it should print "Please, enter just one character", but it is printing "{actual_value}" instead')

    def test_check_ask_letter_right(self):
        f = io.StringIO()
        with redirect_stdout(f):
            with unittest.mock.patch('builtins.input', return_value='a'):
                self.game.ask_letter()
            message = f.getvalue()
        actual_num_letters = self.game.num_letters
        expected_num_letters = self.initial_num_letters - 1
        self.assertEqual(actual_num_letters, expected_num_letters, 'The check_letter method is not reducing the number of letters to be guessed.')
        expected_message = "Nice! a is in the word!\n['_', 'a', '_', '_', '_', '_', '_', '_', '_', '_', '_', 'a', '_', 'a', '_', 'a']\n"
        self.assertEqual(message, expected_message, 'The check_letter method is not working properly for words that are in the word, check that the message has the right format')

    def test_check_ask_letter_wrong_guess(self):
        f = io.StringIO()
        with redirect_stdout(f):
            with unittest.mock.patch('builtins.input', return_value='z'):
                self.game.ask_letter()
            message = f.getvalue()
        actual_num_lives = self.game.num_lives
        expected_num_letters = 4
        self.assertEqual(actual_num_lives, expected_num_letters, 'The check_letter method is not reducing the number of lives. If it does, make sure that the message has the right format and has the exact words as the ones specified in the template')
        expected_message = "Sorry, z is not in the word.\nYou have 4 lives left.\n"
        self.assertEqual(message, expected_message, 'The check_letter method is not working properly for letters that are not in the word. Check that the message has the right format and has the exact words as the ones specified in the template')

    def test_check_repeated(self):
        f = io.StringIO()
        with redirect_stdout(f):
            with patch('builtins.input', return_value='a') as input_mock:
                self.game.ask_letter()
            # actual_value = f.getvalue()
        f = io.StringIO()
        with redirect_stdout(f):  
            with self.assertRaises(Exception) as context:
                with patch('builtins.input', side_effect=['a']) as input_mock:
                    self.game.ask_letter()
            actual_value = f.getvalue()
        expected = 'a was already tried\n'
        self.assertEqual(actual_value, expected, 'The ask_letter method is not checking for repeated words. If it does, make sure that the message has the right format and has the exact words as the ones specified in the template')


if __name__ == '__main__':

    unittest.main(verbosity=0)
    