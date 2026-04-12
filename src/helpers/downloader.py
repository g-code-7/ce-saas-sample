import requests
from pathlib import Path


def download_to_local(url: str, out_path: Path, parent_make_dir: bool = True):
    if not isinstance(out_path, Path):
        raise ValueError(f"{out_path} must be a valid pathlib.Path object.")
    if parent_make_dir:
        out_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        # Send a GET request to the URL
        response = requests.get(url)

        # Raise an exception for bad status codes (4xx, 5xx)
        response.raise_for_status()

        # If successful, print the JSON data
        print("Request was successful!")

        # Write the file out in binary mode to prevent any newline conversions
        out_path.write_bytes(response.content)
        return True

    except requests.exceptions.Timeout:
        print("The request timed out.")
    except requests.exceptions.TooManyRedirects:
        print("There were too many redirects.")
    except requests.exceptions.RequestException as e:
        # Catch any other exceptions, including HTTP errors
        print(f"An error occurred: {e}")
