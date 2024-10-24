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

    run_git_command(['git', 'checkout', 'main'])

def get_descriptors():

    descriptor_list = run_git_command(['git', 'branch', '--list']).split('\n')

    if not descriptor_list:
        return []    
    return [item.strip() for item in descriptor_list if 'main' not in item]

import os
import shutil
import json
import subprocess

def download(deskriptorFolder: str, outputDirPath: str, createJsonDescriptor: bool = False):

    deskriptorFolder = deskriptorFolder.rstrip('/')

    if not '/' in outputDirPath:
        raise RuntimeError(
            'Please define your path using forward slashes.'
        )

    # Normalize the output path
    outputDirPath = os.path.normpath(outputDirPath)

    # Ensure the output directory exists (create if needed)
    if not os.path.exists(outputDirPath):
        os.makedirs(outputDirPath)

    descrikptor_list = get_descriptors()

    if not any(deskriptorFolder in item for item in descrikptor_list):
        raise RuntimeError(f'The required data descriptor was not found. Pick from {descrikptor_list}')
    
    # Run Git command to checkout the correct folder
    run_git_command(['git', 'checkout', f'{deskriptorFolder}'])

    # Get the remote URL of the repository
    try:
        repo_url = run_git_command(['git', 'config', '--get', 'remote.origin.url']).strip()
    except subprocess.CalledProcessError:
        raise RuntimeError("Unable to fetch repository URL from git configuration.")

    if createJsonDescriptor:
        # Build the JSON descriptor
        currentDirPath = os.getcwd()
        srcPath = os.path.join(currentDirPath, deskriptorFolder)

        # Collect metadata information for the JSON descriptor
        metadata = {
            "name": deskriptorFolder,
            "url": repo_url,
            "files": [],
            "pipeline": [],
            "docker": None
        }

        # Walk through the source folder and gather relevant files
        for root, _, files in os.walk(srcPath):
            for file in files:
                # Collect all .json files
                if file.endswith(".json"):
                    metadata["files"].append(file)
                # Collect all Python files for pipelines
                elif file.endswith(".py"):
                    metadata["pipeline"].append(os.path.relpath(os.path.join(root, file), srcPath))
                # Search for Dockerfile descriptor
                elif "dockerfile" in file.lower():
                    metadata["docker"] = os.path.relpath(os.path.join(root, file), srcPath)

        # If no pipelines were found, set it to None
        if not metadata["pipeline"]:
            metadata["pipeline"] = None

        descriptor = {
            "descriptor": {
                "metadata": metadata
            }
        }

        # Write the JSON file to the output directory
        jsonFilePath = os.path.join(outputDirPath, f"{deskriptorFolder}_descriptor.json")
        with open(jsonFilePath, 'w') as jsonFile:
            json.dump(descriptor, jsonFile, indent=2)

        print(f"JSON descriptor created at: {jsonFilePath}")

    else:
        # Destination path for the descriptor folder
        dstPath = os.path.join(outputDirPath, deskriptorFolder)

        # Copy the descriptor folder to the destination if it doesn't exist there
        if not os.path.exists(dstPath):
            currentDirPath = os.getcwd()
            srcPath = os.path.join(currentDirPath, deskriptorFolder)

            # Use shutil.copytree to copy the entire folder
            shutil.copytree(src=srcPath, dst=dstPath)

            print(f"Folder copied to: {dstPath}")



    

    


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

    folder_name = 'descrikptorFolderExample89/'

    utils.generate_example_deskriptor(folder_name)

    upload(folder_name)

    download(folder_name,'data/')

    #merge_branches_to_master()



