import os
from pathlib import Path

from norsvinpy.functions import reusable_function

if __name__ == "__main__":
    main_pth = Path(os.path.realpath(__file__))
    computer_name = os.environ["COMPUTERNAME"]

    website_url = "https://api.github.com/events"
    encoding = reusable_function(lcl_pth=main_pth, computer=computer_name, website=website_url)

    print(f"Hello Norsvin! You have received data encoded in {encoding}")
