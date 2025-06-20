import json
import os

from custom_library.load import load_signed_in

def save_signed_in(signed_in_file, signed_in_users):
    with open(signed_in_file, "w") as f:
        json.dump(list(signed_in_users), f)