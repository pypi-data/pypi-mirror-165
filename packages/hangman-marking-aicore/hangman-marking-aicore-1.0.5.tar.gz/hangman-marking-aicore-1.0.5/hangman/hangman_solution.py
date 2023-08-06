import random

class Hangman:
    def __init__(self, word_list, num_lives=5):
        self.word = random.choice(word_list)
        self.word_guessed = ['_'] * len(self.word)
        self.num_letters = len(set(self.word))
        self.num_lives = num_lives
        self.list_letters = [] # List of letters that have already been tried
        print(f'The mystery word has {len(self.word)} characters')
        print(self.word_guessed)

    
    def check_letter(self, letter):
        if letter in self.word.lower():
            if self.word.count(letter) > 1:
                idx = 0
                for _ in range(self.word.count(letter)):
                    idx = self.word.index(letter, idx)
                    self.word_guessed[idx] = letter
                    idx += 1
            idx = self.word.lower().index(letter)
            self.word_guessed[idx] = letter
            self.num_letters -= 1
            print(f'Nice! {letter} is in the word!')
            print(self.word_guessed)
                
        else:
            self.num_lives -= 1
            print(f'Sorry, {letter} is not in the word.')
            print(f'You have {self.num_lives} lives left.')
        
        self.list_letters.append(letter)

    def ask_letter(self):
        while True:
            letter = input('Enter a character: ').lower()
            
            if letter in self.list_letters:
                print(f"{letter} was already tried")
            elif len(letter) > 1:
                print('Please, enter just one character')
            else:
                break

        self.check_letter(letter)

def play_game(word_list):
    game = Hangman(word_list)

    while True:
        game.ask_letter()
        if game.num_lives == 0:
            print(f'You ran out of lives. The word was {game.word}')
            break
        elif game.num_letters == 0:
            print('Congratulations, you won!')
            break

if __name__ == '__main__':
    word_list = ['apple', 'banana', 'orange', 'pear', 'strawberry', 'watermelon']
    play_game(word_list)