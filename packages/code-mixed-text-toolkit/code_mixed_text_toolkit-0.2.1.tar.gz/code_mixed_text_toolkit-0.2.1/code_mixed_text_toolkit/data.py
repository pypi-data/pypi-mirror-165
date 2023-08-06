import pickle
import json
import pandas as pd
from urllib.request import urlopen

AUTO_FORMATS = {
  "pickle": "pickle",
  "json": "json",
  "txt": "text",
  "text": "text",
  "csv": "csv"
}


FORMATS = {
  "pickle": "A serialized python object, stored using the pickle module.",
  "json": "A serialized python object, stored using the json module.",
  "text": "The raw (unicode string) contents of a file.",
  "csv": "A serialized python object, stored using the pandas module."
}


def load(
  resource_url,
  format="auto",
  encoding=None):
  '''suported resource formats:
    -"txt"
    -"csv"
    -"pickle"
    -"json"
    -"raw"
  '''
  # Determine the format of the resource.
  if format == "auto":
    resource_url_parts = resource_url.split(".")
    ext = resource_url_parts[-1]
    if ext == "gz":
      ext = resource_url_parts[-2]
    format = AUTO_FORMATS.get(ext)
    if format is None:
      raise ValueError(
        "Could not determine format for %s based "
        'on its file\nextension; use the "format" '
        "argument to specify the format explicitly." % resource_url
      )
  
  if format not in FORMATS:
    raise ValueError(f"Unknown format type: {format}!")

  # Load the resource using URL.
  opened_resource = urlopen(resource_url)

  if format == "raw":
    resource_val = opened_resource.read()
  elif format == "pickle":
    resource_val = pickle.load(opened_resource)
  elif format == "json":
    resource_val = json.load(opened_resource)
  elif format == "csv":
    resource_val = pd.read_csv(opened_resource)
  else:
    # The resource is a text format.
    binary_data = opened_resource.read()
    if encoding is not None:
      string_data = binary_data.decode(encoding)
    else:
      try:
        string_data = binary_data.decode("utf-8")
      except UnicodeDecodeError:
        string_data = binary_data.decode("latin-1")
    if format == "text":
      resource_val = string_data

  opened_resource.close()
  return resource_val