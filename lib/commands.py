import os
import sys
import subprocess
import logging
from typing import Union, Tuple, List
from pathlib import Path


def merge_directories(src: Union[str, Path], dest: Union[str, Path], verbose: bool = False):
    """
    Merge 2 directories together instead of putting dest into src
    """
    flags = "" if not verbose else "v"
    os.system(f"rsync -r{flags} {src} {dest}")


def shell(command: List[str]):
    print("dry-run", command)
    # subprocess.run(command, shell=True, check=True, stderr=sys.stderr, stdout=sys.stdout)


def pacman(packages: Tuple[str]):
    shell([f"sudo pacman -Syu {' '.join(packages)}"])


def yay(package: str, index: int):
    logging.info("install from AUR %s -> package id: %s", package, index)
    shell([f"yay -y -a --removemake --answerclean All --answerdiff None {package}"])


def get_home_dir() -> Path:
    output = subprocess.run(["echo $HOME"], shell=True, capture_output=True, text=True, check=True)
    return Path(output.stdout.strip())
