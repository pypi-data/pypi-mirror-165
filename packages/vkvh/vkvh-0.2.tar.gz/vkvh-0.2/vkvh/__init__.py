from pathlib import Path
with open(Path(__file__).parent/"version.txt", "r") as fp:
    __version__=fp.read().strip()
