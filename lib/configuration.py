import os
import logging
from pathlib import Path
from lib.commands import get_home_dir

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
    ("redshift", 1),
]

DOTFILES_REPO = "https://github.com/dhoko/dotfiles.git"
USR_BIN = Path("/usr/local/bin")
logging.basicConfig(
    format="%(levelname)s:[%(filename)s] %(message)s",
    level=os.getenv("LOG_LEVEL", None) or logging.INFO,
)


HOME_DIR = get_home_dir()
CLONED_DIR = HOME_DIR.joinpath("dev", "dotfiles")
SCRIPTS_DIR = CLONED_DIR.joinpath("scripts")
