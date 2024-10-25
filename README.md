# Software Defined Dataset Manager (SDDM) - README

## Overview
The **Software Defined Dataset Manager (SDDM)** is a command-line tool that simplifies managing dataset descriptors in a Git-based version control system. It provides functionalities to upload datasets, download them, and list available dataset descriptors using Git branches.

A dataset descriptor is a collection of JSON files and a Python script (`pipeline.py`) that processes these JSON files to define a specific subset of a large-scale dataset.


## Prerequisites
- Python 3.x
- Git installed and configured
- Python packages: `shutil`, `os`, `subprocess`, `json`

## Installation
Clone the repository and ensure that Git is installed on your system.

```bash
git clone <repository-url>
cd <repository-directory>
```

## Usage
SDDM supports three main commands: upload, download, and get_descriptors.

### Upload a dataset descriptor folder to a new branch in the Git repository.

```bash
python sddm.py upload <deskriptorFolderPath>

deskriptorFolderPath: Path to the descriptor folder.
```

### Download a dataset descriptor to a specified output directory.

```bash
python sddm.py download <deskriptorFolder> <outputDirPath> <createJsonDescriptor>

deskriptorFolder: Name of the descriptor branch to download.
outputDirPath: Path to the directory where the descriptor will be saved.
createJsonDescriptor: Set to True to generate a JSON descriptor (otherwise set to False).

Example:
python sddm.py download descriptorFolderExample ../data/ True
python sddm.py download descriptorFolderExample ../data/ False
```
### Get a list of available dataset descriptors (Git branches).

```bash
python sddm.py get_descriptors
```

## Error Handling
Ensure paths use forward slashes (/).

Check that Git is installed and properly configured.
