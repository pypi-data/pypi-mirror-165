from .verify import get_errors_fails, mark_incomplete, mark_complete
import os

task1_id = '1ef920ef-7e5f-4078-9e28-eb8e08946319'  # Create a new virtual environment
task2_id = '4e351f18-6f0c-44fd-ace7-fda6dad5e8cc'  # Create a new virtual environment - For Users who are on a Mac with an M1 Chip
task3_id = '708b5625-63e0-4aaa-b941-97bb802f4954'  # Complete the installation of dependencies
task4_id = 'bbbdf8bf-d35b-4473-857f-dc81d16edac4'  # Run the model in your local machine
task5_id = 'c41ad504-5f65-4348-9f4c-5cf9b752e477'  # Get familiar with the code

# test_requirements_presence
# test_can_import_opencv
# test_can_import_numpy
# test_can_import_keras

if 'milestone_2.txt' in os.listdir('.'):
    errors = get_errors_fails('milestone_2.txt')

    # If there are no errors, mark everything as complete
    if len(errors) == 0:
        mark_complete(task1_id)
        mark_complete(task2_id)
        mark_complete(task3_id)
        mark_complete(task4_id)
        mark_complete(task5_id)
    # Check if keras_model.h5 is in the repo
    elif 'test_requirements_presence' in errors:
        # mark_incomplete(task2_id, message=errors['test_model_presence'])
        mark_incomplete(task1_id)
        mark_incomplete(task2_id)
        mark_incomplete(task3_id, errors['test_requirements_presence'])

    elif 'test_can_import_numpy' in errors:
        mark_incomplete(task1_id)
        mark_incomplete(task2_id)
        mark_incomplete(task3_id, errors['test_can_import_numpy'])

    elif 'test_can_import_opencv' in errors:
        mark_incomplete(task1_id)
        mark_incomplete(task2_id)
        mark_incomplete(task3_id, errors['test_can_import_opencv'])

    elif 'test_can_import_keras' in errors:
        mark_incomplete(task1_id)
        mark_incomplete(task2_id)
        mark_incomplete(task3_id, errors['test_can_import_keras'])


else:
    mark_incomplete(task1_id)
    mark_incomplete(task2_id)
    mark_incomplete(task3_id)
    mark_incomplete(task4_id)
    mark_incomplete(task5_id)
