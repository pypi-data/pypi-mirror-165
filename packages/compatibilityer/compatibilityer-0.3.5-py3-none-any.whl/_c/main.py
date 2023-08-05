# @converted by compatibilityer.convert.convert

from typing import Type
from compatibilityer.convert import convert_dir
from compatibilityer.converter import Converter
import argparse
from pathlib import Path
import subprocess

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', type=Path, help='directory to convert')
    parser.add_argument('output_dir', type=Path, help='directory to output converted files')
    args = parser.parse_args()
    subprocess.run(['cp', '-r', '-T', args.dir, args.output_dir], check=True)
    convert_dir(args.output_dir, Converter)
if __name__ == '__main__':
    main()