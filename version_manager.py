def write_version(version, path="static/version.txt"):
    """
    Writes the given version number (0–9) to the specified version.txt path.
    Default location is 'static/version.txt' for Flask hosting.
    """
    with open(path, "w") as f:
        f.write(str(version % 10))
    print(f"[Info] Updated version.txt → {version % 10} at {path}")
