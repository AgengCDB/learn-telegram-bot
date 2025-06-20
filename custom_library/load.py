import os
import json
from dotenv import load_dotenv
load_dotenv()

from custom_library.print import print_rd

def load_signed_in(signed_in_file):
    if not os.path.exists(signed_in_file):
        with open(signed_in_file, "w") as f:
            json.dump([], f)
        return set()
    try:
        with open(signed_in_file, "r") as f:
            return set(json.load(f))
    except Exception as e:
        print_rd(f"[ERROR] Could not load signed_in.json: {e}")
        return set()