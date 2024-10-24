import argparse
import subprocess
import sys
import os
import shutil

import utils.utils as utils


def run_git_command(command):
    """Runs a git command using subprocess and returns the output."""
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command {command}: {e.stderr}")
        return None




def upload(deskriptorFolderPath : str):

    if not '/' in deskriptorFolderPath:
        raise RuntimeError(
            'Please define your path using forward slashes.'
        )
    
    deskriptorFolderPath = os.path.normpath(deskriptorFolderPath)

    #deskriptorFolderPath, filename = os.path.split(deskriptorFolderPath)
    if not os.path.isdir(deskriptorFolderPath):
        raise ValueError(
            "Invalid deskriptor path."
        )

    deskriptorFolder = deskriptorFolderPath.split(os.sep)[-1]

    # TODO: check if branch exists

    branches = run_git_command(['git','branch','-l'])

    if not deskriptorFolder in branches:
        # Create and checkout a new branch
        run_git_command(['git', 'checkout', '-b', deskriptorFolder])

    currentDirPath = os.getcwd()

    dstPath = os.path.join(currentDirPath, deskriptorFolder)

    # Copy deskriptorFolderPath into current working directory
    if not os.path.exists(dstPath):
        shutil.copy(src=deskriptorFolderPath, dst= dstPath)

    run_git_command(['git','add', f'{dstPath}'])

    commit_message = "Added software defined dataset."
    
    result = run_git_command(['git','commit', '-m', commit_message])


    print("Uploading software defined dataset to remote...")

    run_git_command(['git', 'push', '--set-upstream',  'origin', f'{deskriptorFolder}'])





    

    
    
    
    
    

    


def merge_branch(branch_name):
    """Merge the pipelines folder from the specified branch into master."""
    print(f"Switching to master branch...")
    run_git_command(['git', 'checkout', 'master'])

    print(f"Merging {branch_name} into master (only pipelines folder)...")
    # Merge the branch, but only merge the 'pipelines' folder
    merge_result = run_git_command(['git', 'merge', '--no-commit', '--no-ff', branch_name])

    # Reset all changes except 'pipelines' folder to prevent merging anything else
    run_git_command(['git', 'reset', 'HEAD', '--', '.'])
    run_git_command(['git', 'checkout', '--', '.'])

    # Now, stage only the 'pipelines' folder for the merge
    run_git_command(['git', 'add', 'pipelines'])

    # Commit the merge, only with 'pipelines'
    commit_message = f"Merged pipelines folder from {branch_name} into master"
    run_git_command(['git', 'commit', '-m', commit_message])

def merge_branches_to_master():
    """Merge pipelines folder from sample1 and sample2 into master."""
    for branch in ['sample1', 'sample2']:
        merge_branch(branch)

    # Push changes (optional)
    print("Pushing changes to remote...")
    run_git_command(['git', 'push', 'origin', 'master'])

if __name__ == "__main__":

    folder_name = 'descrikptorFolderExample3/'

    utils.generate_example_deskriptor(folder_name)

    upload(folder_name)

    #merge_branches_to_master()



