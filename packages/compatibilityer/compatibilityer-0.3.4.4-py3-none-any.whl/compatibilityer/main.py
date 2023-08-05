from typing import Type

from compatibilityer.convert import convert_dir_with_copy
from compatibilityer.converter import Converter

import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("dir", type=Path, help="directory to convert")
    parser.add_argument("output_dir", type=Path, help="directory to output converted files")

    args = parser.parse_args()
    dir_, output_dir = args.dir, args.output_dir
    dir_: Path
    output_dir: Path

    convert_dir_with_copy(dir_, output_dir, Converter)


if __name__ == '__main__':
    main()
