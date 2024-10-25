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
SDDM supports three main commands: upload (or publish), download (or consume), and get_descriptors.

### Publish a dataset descriptor folder to a new branch in the Git repository.

```bash
python sddm.py publish <deskriptorFolderPath>

deskriptorFolderPath: Path to the descriptor folder.
```

### Consume a dataset descriptor to a specified output directory.

```bash
python sddm.py consume <deskriptorFolder> <outputDirPath> 

deskriptorFolder: Name of the descriptor branch to download.
outputDirPath: Path to the directory where the descriptor will be saved.

Example:
python sddm.py download descriptorFolderExample ../data/ True
python sddm.py download descriptorFolderExample ../data/ False
```

Example:
```bash
python sddm.py consume descriptorModelLevelWind ../data/ True
```

### Get a list of available dataset descriptors (Git branches).

```bash
python sddm.py get_descriptors
```

## Error Handling
Ensure paths use forward slashes (/).

Check that Git is installed and properly configured.

## TODO

Publish operation bug: Publish operation only works on folders that are the same level of sddm.py.