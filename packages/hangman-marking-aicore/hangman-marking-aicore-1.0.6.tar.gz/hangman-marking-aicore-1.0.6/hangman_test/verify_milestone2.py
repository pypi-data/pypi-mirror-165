from .verify import get_errors_fails, mark_incomplete, mark_complete
import os
task1_id = '032dcdb6-69e1-450c-96aa-819a45d6aed3' # Fill in the `__init__` method
task2_id = 'c82f56aa-237b-49c6-ba48-67c67e80f569' # Add information to the `ask_letter` method

if 'mileston_2.txt' in os.listdir('.'):

    errors = get_errors_fails('milestone_2.txt')

    if 'test_word' in errors or 'test_word_guessed' in errors or 'test_num_lives' in errors or 'test_num_lives_exists' in errors:
        mark_incomplete(task1_id)
        print('The init method is not set correctly.')
    else:
        mark_complete(task1_id)

    if 'test_check_invalid_input' in errors:
        mark_incomplete(task2_id)
        print(errors['test_check_invalid_input'])
    else:
        mark_complete(task2_id)
else:
    mark_incomplete(task1_id)
    mark_incomplete(task2_id)
