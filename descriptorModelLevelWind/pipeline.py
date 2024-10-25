import xarray
import json
import sys

def run(descriptorjsonFilePath):


    with open(descriptorjsonFilePath, 'r') as jsonFile:
            descriptorDict = json.load(jsonFile)


    valid_time_start = descriptorDict.get('valid_time_start',None)
    valid_time_stop = descriptorDict.get('valid_time_stop',None)

    if not valid_time_start or not valid_time_stop:
         raise RuntimeError(
              'Invalid descriptorFile.'
         )

    ds = xarray.open_zarr(
        'gs://gcp-public-data-arco-era5/co/model-level-wind.zarr-v2',
        chunks=None,
        storage_options=dict(token='anon'),
    )



    model_level_wind = ds.sel(time=slice(ds.attrs['valid_time_start'], ds.attrs['valid_time_stop']))

    print(model_level_wind)

    return 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python pipeline.py run  <path/to/descriptor.json>")
        sys.exit(1)

    run(sys.argv[2])