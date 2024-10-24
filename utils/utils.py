import os
import json

def generate_example_deskriptor(folder_name):
    # Define pipeline name

    pipeline_file = 'etl_pipeline.py'
    # Check if the folder exists, if not, create it
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Find the latest descriptor file number
    descr_files = [f for f in os.listdir(folder_name) if f.startswith("descriktor_") and f.endswith(".json")]
    if descr_files:
        # Sort files and get the highest counter

        latest_file = [ int(item.split('.')[0].split('_')[1]) for item in descr_files] #sorted(descr_files)[-1]
        latest_counter = max(latest_file)
        next_counter = latest_counter + 1
    else:
        next_counter = 0

    # Create new descriptor file
    new_descr_file = f"descriktor_{next_counter}.json"
    descr_path = os.path.join(folder_name, new_descr_file)
    
    # Create an empty JSON file
    with open(descr_path, 'w') as json_file:
        json.dump({}, json_file)

    print(f"Created {new_descr_file}")

    # Ensure the pipeline.py file always exists
    pipeline_path = os.path.join(folder_name, pipeline_file)
    if not os.path.exists(pipeline_path):
        with open(pipeline_path, 'w') as f:
            f.write("# Pipeline script")



