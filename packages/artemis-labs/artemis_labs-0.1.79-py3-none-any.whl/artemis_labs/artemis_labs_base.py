'''
This is the entry point for Artemis
'''

# pylint: disable=line-too-long

import os
import sys
from .artemis_loader import ArtemisLoader

def main() -> None:
    '''
    Entry point when called from command line
    :return: None
    '''

    # Validate input
    if len(sys.argv) == 2 and sys.argv[1] == 'config':
        script_dir = os.path.dirname(os.path.realpath(__file__))
        config_path = os.path.join(script_dir, 'config.py')
        os.system(f"\"{config_path}\"")
        sys.exit(1)

    # Validate input
    if len(sys.argv) < 2:
        print('Artemis Labs: Version 68')
        print("Usage: artemis_labs <./script.py> <python>")
        sys.exit(1)

    # Call command
    runner_path = sys.argv[0].replace('\\', '\\\\')

    # Script path
    script_path = sys.argv[1].strip()
    script_path = script_path.replace('\\', '\\\\')

    # Check cli arg
    launch_command = 'python'
    if len(sys.argv) > 2:
        launch_command = sys.argv[2].strip()

    # Check dev arg
    dev = False
    if len(sys.argv) > 3:
        if sys.argv[3].strip() == "dev":
            print("[Artemis] Running in dev mode")
            dev = True

    # Check launch arg
    launch = True
    if len(sys.argv) > 4:
        if sys.argv[4].strip() == "nolaunch":
            launch = False

    # Process script
    new_path = ArtemisLoader.process_script(runner_path, launch_command, script_path, dev=dev, launch=launch)

    # Run processed script
    print("[Artemis] Running script: " + new_path)
    os.system('python ' + new_path)

def main_direct(runner_path, script_path, launch_command, dev=True, launch=True):
    '''
    Entry point when called from test_runner.py
    :param runner_path: Path to artemis_labs_base
    :param script_path: Path to script to run
    :param launch_command: Command to launch script. Example: python
    :param dev: Whether in dev mode or not
    :param launch: Whether or not to spawn browser
    :return:
    '''

    # Process script
    new_path = ArtemisLoader.process_script(runner_path, launch_command, script_path, dev=dev, launch=launch)

    # Run processed script
    print("[Artemis] Running script: " + new_path)

    os.system('python ' + new_path)

if __name__ == '__main__':
    main()
