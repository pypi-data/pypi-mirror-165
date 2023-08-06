from .verify import get_errors_fails, mark_incomplete, mark_complete
import os

task1_id = '08c1b5f5-7beb-4cec-8189-0f1acc7ca745' # Create an image project model with four different classes: Rock, Paper, Scissors, Nothing
task2_id = 'bcf3c4f1-1547-4727-8e25-a14165eac6d6' # Download the model
task3_id = 'e82a250f-536f-4649-b3e2-2e8680a9119d' # Begin documenting your experience
# test_model_presence
# test_readme_presence

if 'milestone_1.txt' in os.listdir('.'):
    errors = get_errors_fails('milestone_1.txt')


    # If there are no errors, mark everything as complete
    if len(errors) == 0:
        mark_complete(task1_id)
        mark_complete(task2_id)
        mark_complete(task3_id)
    # Check if hangman_solution.py is in the repo
    elif 'test_model_presence' in errors:
        # mark_incomplete(task2_id, message='There is no hangman_solution.py file inside the hangman folder')
        mark_incomplete(task1_id)
        mark_incomplete(task2_id)
        print(errors['test_model_presence'])
    # Check if they are identical
    elif 'test_readme_presence' in errors:
        mark_incomplete(task3_id)
        print(errors['test_readme_presence'])

else:
    mark_incomplete(task1_id)
    mark_incomplete(task2_id)
    mark_incomplete(task3_id)
    print('milestone_1.txt is not in the directory')