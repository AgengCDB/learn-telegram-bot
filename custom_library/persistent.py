from custom_library.load import load_signed_in

# Persistent signed-in storage
SIGNED_IN_FILE = ".config/signed_in.json"
SIGNED_IN_USERS = load_signed_in(signed_in_file=SIGNED_IN_FILE)

COOLDOWN_FILE = ".config/cooldown.json"