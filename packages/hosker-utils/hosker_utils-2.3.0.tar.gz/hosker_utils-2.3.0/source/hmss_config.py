"""
This file lists some configurations for HMSS.
"""

# Standard imports.
from pathlib import Path

##################
# CONFIGURATIONS #
##################

# Components.
PATH_OBJ_TO_HOME = Path.home()

# Defaults.
DEFAULT_BRANCH_NAME = "master"
DEFAULT_EMAIL_ADDRESS = "tomdothosker@gmail.com"
DEFAULT_ENCODING = "utf-8"
DEFAULT_GIT_USERNAME = "tomhosker"
DEFAULT_PLATFORM = "ubuntu"
DEFAULT_PYTHON_VERSION = 3
DEFAULT_ROYAL_REPOS = (
    "chancery",
    "chancery-b",
    "hgmj",
    "hoskers-almanack",
    "hosker_utils",
    "kingdom-of-cyprus",
    "lucifer-in-starlight",
    "vanilla_web"
)
DEFAULT_TARGET_DIR = str(PATH_OBJ_TO_HOME)
CODE_INDENTATION = 4

# Default paths.
DEFAULT_PATH_TO_HMSS_CONFIG_FILE = str(PATH_OBJ_TO_HOME/"hmss_config.json")
DEFAULT_PATH_TO_GIT_CREDENTIALS = str(PATH_OBJ_TO_HOME/".git-credentials")
DEFAULT_PATH_TO_PAT = str(PATH_OBJ_TO_HOME/"personal_access_token.txt")
DEFAULT_PATH_TO_WALLPAPER_DIR = str(PATH_OBJ_TO_HOME/"hmss"/"wallpaper")

# Command elements.
INTERNAL_PYTHON_COMMAND = "python3"
