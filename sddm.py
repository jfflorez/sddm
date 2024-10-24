import argparse
import subprocess
import sys
import os
import shutil
import json

import utils.utils as utils


def run_git_command(command):
    """Runs a git command using subprocess and returns the output."""
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command {command}: {e.stderr}")
        return None


def upload(deskriptorFolderPath: str):
    if not '/' in deskriptorFolderPath:
        raise RuntimeError(
            'Please define your path using forward slashes.'
        )

    deskriptorFolderPath = os.path.normpath(deskriptorFolderPath)

    if not os.path.isdir(deskriptorFolderPath):
        raise ValueError(
            "Invalid deskriptor path."
        )

    deskriptorFolder = deskriptorFolderPath.split(os.sep)[-1]

    branches = run_git_command(['git', 'branch', '-l'])

    if not deskriptorFolder in branches:
        # Create and checkout a new branch
        run_git_command(['git', 'checkout', '-b', deskriptorFolder])

    currentDirPath = os.getcwd()
    dstPath = os.path.join(currentDirPath, deskriptorFolder)

    # Copy deskriptorFolderPath into current working directory
    if not os.path.exists(dstPath):
        shutil.copy(src=deskriptorFolderPath, dst=dstPath)

    run_git_command(['git', 'add', f'{dstPath}'])

    commit_message = "Added software defined dataset."
    result = run_git_command(['git', 'commit', '-m', commit_message])

    print("Uploading software defined dataset to remote...")
    run_git_command(['git', 'push', '--set-upstream', 'origin', f'{deskriptorFolder}'])

    run_git_command(['git', 'checkout', 'main'])


def get_descriptors():
    descriptor_list = run_git_command(['git', 'branch', '--list']).split('\n')
    if not descriptor_list:
        return []
    return [item.strip() for item in descriptor_list if 'main' not in item]


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

    # Check if the branch exists remotely
    branch_list_remote = run_git_command(['git', 'branch', '--list', '-r'])

    # If the branch is not in the descriptor list, fetch it
    if not any(deskriptorFolder in item for item in descrikptor_list):  
        if any(f'origin/{deskriptorFolder}' in branch for branch in branch_list_remote.splitlines()):
            print(f"Fetching branch {deskriptorFolder} from the remote repository...")
            try:
                run_git_command(['git', 'fetch', 'origin', deskriptorFolder])
            except RuntimeError as e:
                raise RuntimeError(f"Failed to fetch branch '{deskriptorFolder}': {e}")
        else:
            raise RuntimeError(f'The required data descriptor was not found. Pick from {descrikptor_list}')

    # Run Git command to checkout the correct branch
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
                if file.endswith(".json"):
                    metadata["files"].append(file)
                elif file.endswith(".py"):
                    metadata["pipeline"].append(os.path.relpath(os.path.join(root, file), srcPath))
                elif "dockerfile" in file.lower():
                    metadata["docker"] = os.path.relpath(os.path.join(root, file), srcPath)

        if not metadata["pipeline"]:
            metadata["pipeline"] = None

        descriptor = {
            "descriptor": {
                "metadata": metadata
            }
        }

        # Write the JSON file to the output directory
        jsonFilePath = os.path.join(outputDirPath, f"{deskriptorFolder}.json")
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


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <function_name> <function_args>")
        sys.exit(1)

    # Extract the function name from the command line arguments
    function_name = sys.argv[1]

    # Handle function execution based on the provided function name
    if function_name == "upload":
        if len(sys.argv) != 3:
            print("Usage: python sddm.py upload <deskriptorFolderPath>")
            sys.exit(1)
        deskriptorFolderPath = sys.argv[2]
        upload(deskriptorFolderPath)

    elif function_name == "download":
        if len(sys.argv) != 5:
            print("Usage: python sddm.py download <deskriptorFolder> <outputDirPath> <createJsonDescriptor(True|False)>")
            sys.exit(1)
        arg1 = sys.argv[2]
        arg2 = sys.argv[3]
        arg3 = sys.argv[4] == 'True'
        download(arg1, arg2, arg3)

    elif function_name == "get_descriptors":
        if len(sys.argv) != 2:
            print("Usage: python sddm.py get_descriptors")
            sys.exit(1)
        descriptors = get_descriptors()
        print("Available descriptors:", descriptors)

    else:
        print(f"Error: Unknown function '{function_name}'")
        sys.exit(1)



#if __name__ == "__main__":

#    folder_name = 'descrikptorFolderExample888/'

#    utils.generate_example_deskriptor(folder_name)

#    upload(folder_name)

#    download(folder_name,'data/',True)

    #merge_branches_to_master()



