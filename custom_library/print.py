from datetime import datetime

# ANSI color codes
RESET   = "\033[0m"
RED     = "\033[91m"
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
BLUE    = "\033[94m"
MAGENTA = "\033[95m"
CYAN    = "\033[96m"
WHITE   = "\033[97m"

def _timestamp():
    return datetime.now().strftime("[%Y%m%d_%H%M%S]")

def print_rd(text: str):
    try:
        print(f"{RED}{_timestamp()} {text}{RESET}")
    except:
        print("")

def print_gr(text: str):
    try:
        print(f"{GREEN}{_timestamp()} {text}{RESET}")
    except:
        print("")

def print_yl(text: str):
    try:
        print(f"{YELLOW}{_timestamp()} {text}{RESET}")
    except:
        print("")

def print_bl(text: str):
    try:
        print(f"{BLUE}{_timestamp()} {text}{RESET}")
    except:
        print("")

def print_mg(text: str):
    try:
        print(f"{MAGENTA}{_timestamp()} {text}{RESET}")
    except:
        print("")

def print_cy(text: str):
    try:
        print(f"{CYAN}{_timestamp()} {text}{RESET}")
    except:
        print("")

def print_wh(text: str):
    try:
        print(f"{WHITE}{_timestamp()} {text}{RESET}")
    except:
        print("")

def print_nt(text: str):
    try:
        print(f"{_timestamp()} {text}")
    except:
        print("")
