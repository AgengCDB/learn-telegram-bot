def load_allowed_users(file_path="allowed_users.txt"):
    try:
        with open(file_path, "r") as f:
            return [
                int(line.strip())
                for line in f
                if line.strip() and not line.strip().startswith("#")
            ]
    except FileNotFoundError:
        print("allowed_users.txt not found.")
        return []