# Software Defined Dataset (SDD) Store - README

## Overview

The **Software Defined Dataset Store (SDD Store)** is a Git-based repository for managing **software-defined datasets (SDDs)**. Each SDD is a collection of JSON files that specify a dataset subset, along with a Python script (`etl_pipeline.py`) that processes the SDD to retrieve this subset from large, petabyte-scale datasets that are too large to store locally.


The repository structure includes:
- **Main branch**: Contains the **Software Defined Dataset Manager (SDDM)**, a command-line tool for managing SDDs.
- **Dataset branches**: Each branch holds a distinct software-defined dataset.

### Key Features
The **SDDM** tool provides a streamlined interface to:
- Upload new SDDs to the store
- Download existing SDDs
- List available datasets along with their descriptors (metadata about each SDD’s contents, structure, and purpose)


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
### Get a list of available dataset descriptors (Git branches).

```bash
python sddm.py get_descriptors
```

## Error Handling
Ensure paths use forward slashes (/).

Check that Git is installed and properly configured.

## TODO

Publish operation bug: Publish operation only works on folders that are the same level of sddm.py.