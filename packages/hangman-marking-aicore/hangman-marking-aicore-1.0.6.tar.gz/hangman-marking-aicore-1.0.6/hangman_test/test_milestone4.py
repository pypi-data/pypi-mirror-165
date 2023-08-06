from hangman.hangman_solution import Hangman
from hangman.hangman_solution import play_game
import unittest
from contextlib import redirect_stdout
import io
from unittest.mock import patch
import os
import spacy
import pkgutil
class HangmanTestCase(unittest.TestCase):

    def setUp(self):
        word_list = ['WatermelonBanana']
        f = io.StringIO()
        with redirect_stdout(f):
            self.game = Hangman(word_list, 5)
        self.init_message = f.getvalue()

    def test_play_win(self):
        f = io.StringIO()
        with redirect_stdout(f):
            with patch('builtins.input', side_effect=['W', 'a', 't', 'e', 'r', 'm', 'l', 'o', 'n', 'b']) as input_mock:
                play_game(['WatermelonBanana'])
        actual_value = f.getvalue()
        actual_last = actual_value.split('\n')[-2]
        expected = "Congratulations, you won!"
        self.assertEqual(actual_last, expected, 'The play_game method is not working properly when you win the game. Check that the message has the right format and that you haven\'t added extra spaces or changed a letter in the sentence')

    def test_play_lose(self):
        f = io.StringIO()
        with redirect_stdout(f):
            with patch('builtins.input', side_effect=['z', 's', 'p', 'q', 'v']) as input_mock:
                play_game(['WatermelonBanana'])
        actual_value = f.getvalue()
        actual_last = actual_value.split('\n')[-2]
        expected = "You ran out of lives. The word was WatermelonBanana"
        self.assertEqual(actual_last, expected, 'The play_game method is not working properly when you run out of lives. Check that the message has the right format and that you haven\'t added extra spaces or changed a letter in the sentence')

    def test_presence_readme(self):
        self.assertIn('README.md', os.listdir('.'), 'You should have a README.md file in your project folder')
        with open('README.md', 'r') as f:
            readme = f.read()
        self.assertGreater(len(readme), 2500, 'The README.md file should be at least 2500 characters long')
        nlp = spacy.load("en_core_web_md")
        tdata = str(pkgutil.get_data(__name__, "documentation.md"))
        doc_1 = nlp(readme)
        doc_2 = nlp(tdata)
        self.assertLessEqual(doc_1.similarity(doc_2), 0.975, 'The README.md file is almost identical to the one provided in the template')
        
        

        
if __name__ == '__main__':

    unittest.main(verbosity=2)
    