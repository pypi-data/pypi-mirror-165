from golfer.golf import golf

import argparse
from pathlib import Path
import ast
import subprocess
import time


def convert(code: str) -> str:
    return golf(code)


def convert_file(code: str) -> str:
    return convert(code)


def convert_dir(dir_: Path) -> None:
    assert dir_.is_dir()
    for file in dir_.glob('**/*.py'):
        with open(file, "r") as f:
            c = f.read()
            ast.parse(c)
        with open(file, "w") as f:
            nc = convert_file(c)
            f.write(nc)


def convert_dir_with_copy(dir_: Path, output_dir: Path) -> None:
    excludes = []

    if output_dir in dir_.glob("**/*"):
        excludes.append(output_dir)

    excludes = ["--exclude", *map(str, excludes)] if excludes else []

    subprocess.run(["rsync", "-a", str(dir_) + "/", str(output_dir) + "/", *excludes], check=True)

    convert_dir(output_dir)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("dir", type=Path, help="directory to convert")
    parser.add_argument("output_dir", type=Path, help="directory to output converted files")

    args = parser.parse_args()
    dir_, output_dir = args.dir, args.output_dir
    dir_: Path
    output_dir: Path

    convert_dir_with_copy(dir_, output_dir)


if __name__ == '__main__':
    main()
