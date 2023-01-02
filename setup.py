"""
Autosetup ArchLinux Endeavour OS
================================

Install a few dependencies
    - git-lfs
    - gpg-agent (if not already there)
    - tmux
    - zsh
    - unzip
    - unrar
    - htop
    - fzf
    - ripgrep
    - jq
    - vlc
    - tree
    - ntfs-3g
    - bat
    - gettext
    - coreutils
    - synapse
    - imagemagick
    - xz (lzm)
    - guake (terminal)
    - alacritty (terminal)
    - sakura (terminal)
    - brave browser
    - firefox
    - chromium
    - celluloid (mpv UI)
    - mpv
    - clementine (Music player)
    - kazam (record my desktop)
    - mousepad (text editor)
    - neovim
    - vim
    - mcomix
    - docker
    - gimp 
    - pinta
    - pandoc
    - pcmanfm
    - protonvpn
    - virt manager (qemu + kvm)
    - Helix editor
    - glow (markdown render cli)
    - kubectl
    - kubens
    - k9s
    - helm
    - z 

Bonus:
- Yaru themes
- nvidia drivers
"""

import os
import sys
import subprocess
import logging
from typing import Union, Tuple, List
from pathlib import Path
from dataclasses import dataclass, field

BASE_UTILS = ("git-lfs", "zsh", "unzip", "unrar", "tree", "coreutils", "gettext", "ntfs-3g", "xz")
BASE_APPS = (
    "z",
    "tmux",
    "htop",
    "neovim",
    "vim",
    "pandoc",
    "pcmanfm",
    "mousepad",
    "celluloid",
    "guake",
    "imagemagick",
    "synapse",
    "vlc",
    "bat",
    "jq",
    "fzf",
    "ripgrep",
    "virt-manager",
    "gimp",
    "pinta",
    "clementine",
    "alacritty",
    "chromium",
    "docker",
    "kubectl",
    "k9s",
    "kubens",
    "glow",
    "helm",
    "helix",
)

AUR_APPS = [
    ("sakura", 1),
    ("brave", 1),
    ("kazam", 1),
    ("mcomix", 1),
    ("amber-search-git", 1),
    ("protonvpn", 2),
    ("sublime-text-4", 1),
]

DOTFILES_REPO = "https://github.com/dhoko/dotfiles.git"
USR_BIN = Path("/usr/local/bin")
logging.basicConfig(
    format="%(levelname)s:[%(filename)s] %(message)s",
    level=os.getenv("LOG_LEVEL", None) or logging.INFO,
)


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


HOME_DIR = get_home_dir()
CLONED_DIR = HOME_DIR.joinpath("dev", "dotfiles")
SCRIPTS_DIR = CLONED_DIR.joinpath("scripts")


@dataclass
class File:
    name: str
    output: str = ""
    source_dir: Path = CLONED_DIR
    dest_dir: Path = HOME_DIR
    sudo: bool = False

    def __post_init__(self):
        self.output = self.output or self.name

    def get_src(self) -> Path:
        return self.source_dir.joinpath(self.name)

    def get_dest(self) -> Path:
        return self.dest_dir.joinpath(self.output)


@dataclass
class Todo:
    scope: str
    entries: List[File] = field(default_factory=list)

    def run(self):
        logging.info("load configuration for: %s", self.scope)
        for entry in self.entries:
            command = f"ln -s {entry.get_src()} {entry.get_dest()}"
            if entry.sudo:
                command = f"sudo {command}"
            shell([command])


def load_dotfiles():

    if not CLONED_DIR.parent.exists():
        CLONED_DIR.parent.mkdir()

    shell([f"git clone '{DOTFILES_REPO}' --depth 1 {CLONED_DIR}"])

    TODOS = [
        Todo(
            scope="finder",
            entries=[File(sudo=True, name="finder", source_dir=SCRIPTS_DIR, dest_dir=USR_BIN)],
        ),
        Todo(scope="tmux", entries=[File(name=".tmux"), File(name=".tmux.conf")]),
        Todo(
            scope="shell configuration (bash, zsh)",
            entries=[
                File(name=".bashrc.d"),
                File(name=".zshrc"),
            ],
        ),
        Todo(scope="applications config", entries=[File(name=".vimrc")]),
        Todo(
            scope="alias helix editor to hx",
            entries=[
                File(
                    sudo=True,
                    name="helix",
                    output="hx",
                    source_diff=Path("/usr/bin"),
                    dest_dir=USR_BIN,
                )
            ],
        ),
    ]

    for todo in TODOS:
        todo.run()


def main():

    print(
        """
Missing packages:
    - nodejs
    - nvm
    From PIP:
        - litecli
        - pyenv
        - pipenv
    From NPM:
        - yarn
        - npm-check
        
Credentials:
    - git config from home dir (not uptodate inside github)
    - git config proton (~.gitconfig.*)
    - k8s config (~/.kube)
    - ssh keys
    - gpg keys
    - glcoud (~/.config/gcloud)
    - kubectl
    - protonvpn
    - Google Chrome/Brave/Firefox       
    - docker (~/.docker)
LSP definitions:
    - typescript
    - json
    - python
    - golang
    - yaml

Todo:
    - Alias binary helix to hx
"""
    )

    load_dotfiles()
    return False

    # shell(
    # [
    #     "echo Hello, what is your name?' && read name && echo \"Hello: $name\""
    # ],
    # )

    logging.info("install base utilities for the OS")
    pacman(BASE_UTILS)

    logging.info("install base apps for the OS")
    pacman(BASE_APPS)

    for (package, index) in AUR_APPS:
        yay(package, index)

    shell(
        [
            'sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"'
        ]
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        logging.error(err)
        sys.exit(1)
