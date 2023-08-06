from .verify import get_errors_fails, mark_incomplete, mark_complete
import os

task1_id = '3f496682-807d-4ba4-aa64-c09ebba9b83a' # Download the template
task2_id = '4c240b07-e0b2-421a-9cfc-2df6858c9f54' # Create your solution file
task3_id = '62158fc2-ba1d-49f4-aee0-66ec01f63baa' # Fill in the `ask_letter` function


if 'milesone_1.txt' in os.listdir('.'):
    errors = get_errors_fails('milestone_1.txt')


    # If there are no errors, mark everything as complete
    if len(errors) == 0:
        mark_complete(task1_id)
        mark_complete(task2_id)
        mark_complete(task3_id)
    # Check if hangman_solution.py is in the repo
    elif 'test_presence' in errors:
        # mark_incomplete(task2_id, message='There is no hangman_solution.py file inside the hangman folder')
        mark_incomplete(task2_id)
        mark_incomplete(task3_id)
        print(errors['test_presence'])
    # Check if they are identical
    elif 'test_diff' in errors:
        mark_incomplete(task3_id)
        print(errors['test_diff'])

        # mark_incomplete(task3_id, message='No changes were made to hangman_solution.py')
    elif 'test_presence_ask_letter' in errors:
        # mark_incomplete(task3_id, message='The play_game() function is not using the ask_letter method')
        mark_incomplete(task3_id)
        print(errors['test_presence_ask_letter'])

else:
    mark_incomplete(task1_id)
    mark_incomplete(task2_id)
    mark_incomplete(task3_id)


