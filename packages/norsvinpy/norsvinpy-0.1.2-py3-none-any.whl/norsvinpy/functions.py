from pathlib import Path

import requests


def reusable_function(lcl_pth: Path, computer: str, website: str = "https://api.github.com/events") -> str:
    """
    Description of the reusable function

    Args:
        lcl_pth (Path): the path of the file of interest
        computer (str): the name of the super computer
        website (str): the website we want to query (default is 'https://api.github.com/events')

    Returns:
        str: how the data is encoded
    """
    #
    print(f"FoI: {lcl_pth} on computer {computer}")
    #
    r = requests.get(website)
    print(f"Status code: {r.status_code}")
    return r.encoding
