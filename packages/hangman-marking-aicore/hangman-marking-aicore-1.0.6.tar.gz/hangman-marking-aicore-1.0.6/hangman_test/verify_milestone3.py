from .verify import get_errors_fails, mark_incomplete, mark_complete
import os

task1_id = 'c82f56aa-237b-49c6-ba48-67c67e80f569' # Run some checks
task2_id = '2f2ccea4-f88e-4bbe-8063-1a3cf77c6d6d' # What happens when the letter is in the word?
task3_id = '04dc4041-10bf-4c02-84cd-892b1913adf4' # What happens when the letter is NOT in the word?
task4_id = '6618e92e-a15d-44c1-91a3-e33878f19d02' # Complete the `ask_letter` method

# test_check_ask_letter_right
# test_check_ask_letter_wrong_guess
# test_check_repeated
# test_check_invalid_input

if 'milestone_3.txt' in os.listdir('.'):
    errors = get_errors_fails('milestone_3.txt')

    if 'test_check_invalid_input' in errors:
        mark_incomplete(task1_id, errors['test_check_invalid_input'])
        mark_incomplete(task2_id)
        mark_incomplete(task3_id)
        mark_incomplete(task4_id)

    elif 'test_check_repeated' in errors:
        mark_incomplete(task1_id, errors['test_check_repeated'])
        mark_incomplete(task2_id)
        mark_incomplete(task3_id)
        mark_incomplete(task4_id)

    elif 'test_check_ask_letter_right' in errors:
        mark_complete(task1_id)
        mark_incomplete(task2_id, errors['test_check_ask_letter_right'])
        mark_incomplete(task3_id)
        mark_incomplete(task4_id)

    elif 'test_check_ask_letter_wrong_guess' in errors:
        mark_complete(task1_id)
        mark_complete(task2_id)
        mark_incomplete(task3_id, errors['test_check_ask_letter_wrong_guess'])
        mark_incomplete(task4_id)
    else:
        mark_complete(task1_id)
        mark_complete(task2_id)
        mark_complete(task3_id)
        mark_complete(task4_id)

else:
    mark_incomplete(task1_id)
    mark_incomplete(task2_id)
    mark_incomplete(task3_id)
    mark_incomplete(task4_id)