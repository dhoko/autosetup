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
import logging
import argparse
from typing import Union, Tuple, List
from pathlib import Path
from dataclasses import dataclass, field
from lib.configuration import (
    BASE_UTILS,
    BASE_APPS,
    AUR_APPS,
    DOTFILES_REPO,
    USR_BIN,
    HOME_DIR,
    USR_BIN,
    CLONED_DIR,
    SCRIPTS_DIR,
)
from lib.commands import pacman, yay, shell

parser = argparse.ArgumentParser(description="install os")
parser.add_argument("--bin", action="store_true", help="Install binaries")
parser.add_argument("--config", action="store_true", help="Install configuration")
args = parser.parse_args()


def install_remote_projects():
    logging.info("Add oh-my-zsh")
    shell(
        [
            'sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"'
        ]
    )


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
            output_file = entry.get_dest()
            if output_file.exists():
                output_file.rename(Path(output_file.parent, f"{output_file}.back"))

            command = f"ln -s {entry.get_src()} {entry.get_dest()}"
            if entry.sudo:
                command = f"sudo {command}"
            shell([command])


def load_dotfiles():
    if not CLONED_DIR.parent.exists():
        CLONED_DIR.parent.mkdir()

    shell([f"git clone '{DOTFILES_REPO}' --depth 1 {CLONED_DIR} --quiet"])


def import_files():
    for todo in [
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
                    source_dir=Path("/usr/bin"),
                    dest_dir=USR_BIN,
                )
            ],
        ),
    ]:
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

"""
    )

    # shell(
    # [
    #     "echo Hello, what is your name?' && read name && echo \"Hello: $name\""
    # ],
    # )

    if args.bin:
        logging.info("install base utilities for the OS")
        pacman(BASE_UTILS)

        logging.info("install base apps for the OS")
        pacman(BASE_APPS)

        for package, index in AUR_APPS:
            yay(package, index)

        install_remote_projects()

    if args.config:
        load_dotfiles()
        import_files()


if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        logging.error(err)
        sys.exit(1)
