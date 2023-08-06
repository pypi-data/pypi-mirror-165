from .verify import get_errors_fails, mark_incomplete, mark_complete
import os

task1_id = '6abbafb7-59a3-481a-9b1f-837e37b5826c' # Code the logic of the game
task2_id = '33a3d741-121f-4a7a-aa2c-b0eeae1c0c0a' # Take it even further! (Bonus Points)
task3_id = 'f9464de6-74a0-43f7-aa62-91f2677b267f' # Document your experience
# test_play_lose 
# test_play_win 
# test_presence_readme

if 'milestone_4.txt' in os.listdir('.'):
    errors = get_errors_fails('milestone_4.txt')

    if 'test_play_lose' in errors or 'test_play_win' in errors:
        
        mark_incomplete(task2_id)
        if 'test_play_lose' in errors:
            mark_incomplete(task1_id, errors['test_play_lose'])
            mark_incomplete(task2_id)
        else:
            mark_incomplete(task1_id, errors['test_play_win'])
            mark_incomplete(task2_id)
    else:
        mark_complete(task1_id)

    if 'test_presence_readme' in errors:
        mark_incomplete(task3_id, errors['test_presence_readme'])
    else:
        mark_complete(task3_id)

    if len(errors) == 0:
        mark_complete(task2_id)

else:
    mark_incomplete(task1_id)
    mark_incomplete(task2_id)
    mark_incomplete(task3_id)
