"""
This code defines a class which installs the various packages and repositories
required on this computer.
"""

# Standard imports.
import contextlib
import json
import logging
import os
import shutil
import subprocess
import urllib.parse
import warnings
from dataclasses import dataclass, field
from pathlib import Path
from typing import ClassVar

# Local imports.
from .git_credentials import set_up_git_credentials
from .hmss_config import (
    CODE_INDENTATION,
    DEFAULT_BRANCH_NAME,
    DEFAULT_PATH_TO_GIT_CREDENTIALS,
    DEFAULT_PATH_TO_PAT,
    DEFAULT_PLATFORM,
    DEFAULT_GIT_USERNAME,
    DEFAULT_EMAIL_ADDRESS,
    DEFAULT_PATH_TO_HMSS_CONFIG_FILE,
    DEFAULT_PATH_TO_WALLPAPER_DIR,
    DEFAULT_ROYAL_REPOS,
    DEFAULT_TARGET_DIR,
    INTERNAL_PYTHON_COMMAND
)

# Local constants.
DEFAULT_HMSS_ARGUMENT_DICT = {
    "this_platform": DEFAULT_PLATFORM,
    "target_dir": DEFAULT_TARGET_DIR,
    "thunderbird_num": None,
    "path_to_git_credentials": DEFAULT_PATH_TO_GIT_CREDENTIALS,
    "path_to_pat": DEFAULT_PATH_TO_PAT,
    "git_username": DEFAULT_GIT_USERNAME,
    "email_address": DEFAULT_EMAIL_ADDRESS,
    "path_to_wallpaper_dir": DEFAULT_PATH_TO_WALLPAPER_DIR,
    "royal_repos": DEFAULT_ROYAL_REPOS,
    "test_run": False,
    "show_output": False,
    "minimal": True
}

##############
# MAIN CLASS #
##############

@dataclass
class HMSoftwareInstaller:
    """ The class in question. """
    # Fields
    this_platform: str = DEFAULT_PLATFORM
    target_dir: str = DEFAULT_TARGET_DIR
    thunderbird_num: int = None
    path_to_git_credentials: str = DEFAULT_PATH_TO_GIT_CREDENTIALS
    path_to_pat: str = DEFAULT_PATH_TO_PAT
    git_username: str = DEFAULT_GIT_USERNAME
    email_address: str = DEFAULT_EMAIL_ADDRESS
    path_to_wallpaper_dir: str = DEFAULT_PATH_TO_WALLPAPER_DIR
    royal_repos: tuple = DEFAULT_ROYAL_REPOS
    test_run: bool = False
    show_output: bool = False
    minimal: bool = True
    failure_log: list = field(default_factory=list)
    git_logger: logging.Logger = None

    # Class attributes.
    BASHRC_ADDITION: ClassVar[str] = "back-up-royal-repos &>/dev/null & disown"
    CHROME_DEB: ClassVar[str] = "google-chrome-stable_current_amd64.deb"
    CHROME_STEM: ClassVar[str] = "https://dl.google.com/linux/direct/"
    EXPECTED_PATH_TO_GOOGLE_CHROME_COMMAND: ClassVar[str] = \
        "/usr/bin/google-chrome"
    GIT_CLONE: ClassVar[tuple] = ("git", "clone")
    GIT_FETCH: ClassVar[tuple] = ("git", "fetch", "--all")
    GIT_LOG_FILENAME: ClassVar[str] = "hm_git.log"
    GIT_LOG_FORMAT: ClassVar[str] = "%(asctime)s | %(levelname)s | %(message)s"
    GIT_PULL: ClassVar[tuple] = ("git", "pull", "origin", DEFAULT_BRANCH_NAME)
    GIT_URL_STEM: ClassVar[str] = "https://github.com/"
    INTERNAL_PYTHON_COMMAND: ClassVar[str] = INTERNAL_PYTHON_COMMAND
    MISSING_FROM_CHROME: ClassVar[tuple] = ("eog", "nautilus")
    OTHER_THIRD_PARTY: ClassVar[tuple] = ("gedit-plugins", "inkscape")
    PATH_TO_BASHRC: ClassVar[str] = str(Path.home()/".bashrc")
    SUPPORTED_PLATFORMS: ClassVar[set] = {
        "ubuntu", "chrome-os", "raspian", "linux-based"
    }
    WALLPAPER_EXT: ClassVar[str] = ".png"
    WALLPAPER_STEM: ClassVar[str] = "wallpaper_t"

    def __post_init__(self):
        self.git_logger = self.make_git_logger()

    def make_git_logger(self):
        """ Construct our Git logging object. """
        result = logging.getLogger()
        result.setLevel(logging.INFO)
        formatter = logging.Formatter(self.GIT_LOG_FORMAT)
        path_to_log = str(Path(self.target_dir)/self.GIT_LOG_FILENAME)
        file_handler = logging.FileHandler(path_to_log)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        result.addHandler(file_handler)
        return result

    def make_essentials(self):
        """ Build a tuple of essential processes to run. """
        result = (
            {
                "imperative": "Check Platform",
                "gerund": "Checking Platform",
                "method": self.check_platform
            }, {
                "imperative": "Update and upgrade",
                "gerund": "Updating and upgrading",
                "method": self.update_and_upgrade
            }, {
                "imperative": "Set up Git",
                "gerund": "Setting up Git",
                "method": self.set_up_git
            }
        )
        return result

    def make_non_essentials(self):
        """ Build a tuple of non-essential processes to run. """
        result = (
            {
                "imperative": "Install Google Chrome",
                "gerund": "Installing Google Chrome",
                "method": self.install_google_chrome
            }, {
                "imperative": "Install other third party",
                "gerund": "Installing other third party",
                "method": self.install_other_third_party
            }, {
                "imperative": "Clone royal repos",
                "gerund": "Cloning royal repos",
                "method": self.clone_royal_repos
            }, {
                "imperative": "Schedule royal repo backups",
                "gerund": "Scheduling royal repo backups",
                "method": self.schedule_royal_repo_backups
            }
        )
        return result

    def run_with_indulgence(self, arguments):
        """ Run a command, and don't panic immediately if we get a non-zero
        return code. """
        if self.test_run:
            return True
        if self.show_output:
            print("Running subprocess.run() with arguments:")
            print(arguments)
            try:
                subprocess.run(arguments, check=True)
            except subprocess.CalledProcessError:
                return False
        else:
            try:
                subprocess.run(arguments, check=True, stdout=subprocess.DEVNULL)
            except subprocess.CalledProcessError:
                return False
        return True

    def install_via_apt(self, package_name, command=None):
        """ Attempt to install a package, and tell me how it went. """
        if not command:
            command = package_name
        if check_command_exists(command):
            return True
        arguments = ["sudo", "apt-get", "install", package_name, "--yes"]
        if self.run_with_indulgence(arguments):
            return True
        return False

    def check_platform(self):
        """ Test whether the platform we're using is supported. """
        if self.this_platform in self.SUPPORTED_PLATFORMS:
            return True
        return False

    def set_up_git(self):
        """ Install Git and set up a personal access token. """
        install_result = self.install_via_apt("git")
        if not install_result:
            return False
        pat_result = \
            set_up_git_credentials(
                username=self.git_username,
                email_address=self.email_address,
                path_to_git_credentials=self.path_to_git_credentials,
                path_to_pat=self.path_to_pat
            )
        if not pat_result:
            return False
        return True

    def install_google_chrome(self):
        """ Ronseal. """
        if (
            check_command_exists("google-chrome") or
            (self.this_platform == "chrome-os")
        ):
            return True
        chrome_url = urllib.parse.urljoin(self.CHROME_STEM, self.CHROME_DEB)
        chrome_deb_path = "./"+self.CHROME_DEB
        if not self.run_with_indulgence(["wget", chrome_url]):
            return False
        if not self.install_via_apt(chrome_deb_path):
            return False
        os.remove(chrome_deb_path)
        return True

    def change_wallpaper(self):
        """ Change the wallpaper on the desktop of this computer. """
        if not Path(self.path_to_wallpaper_dir).exists():
            return False
        if self.thunderbird_num:
            wallpaper_filename = (
                self.WALLPAPER_STEM+
                str(self.thunderbird_num)+
                self.WALLPAPER_EXT
            )
        else:
            wallpaper_filename = "default.jpg"
        wallpaper_path = \
            str(Path(self.path_to_wallpaper_dir)/wallpaper_filename)
        if self.this_platform == "ubuntu":
            arguments = [
                "gsettings",
                "set",
                "org.gnome.desktop.background",
                "picture-uri",
                "file:///"+wallpaper_path
            ]
        elif self.this_platform == "raspbian":
            arguments = ["pcmanfm", "--set-wallpaper", wallpaper_path]
        else:
            return False
        result = self.run_with_indulgence(arguments)
        return result

    def make_git_url(self, repo_name):
        """ Make the URL pointing to a given repo. """
        suffix = self.git_username+"/"+repo_name+".git"
        result = urllib.parse.urljoin(self.GIT_URL_STEM, suffix)
        return result

    def clone_repo(self, repo_name):
        """ Clone a given repo. """
        with change_working_directory(self.target_dir):
            if Path(repo_name).exists():
                warnings.warn("Looks like "+repo_name+" already exists...")
                return True
            arguments = list(self.GIT_CLONE)+[self.make_git_url(repo_name)]
            if not self.run_with_indulgence(arguments):
                self.git_logger.error("Problem cloning repo: %s", repo_name)
                return False
        return True

    def clone_royal_repos(self):
        """ Clone ALL royal repos. """
        result = True
        for repo in self.royal_repos:
            if not self.clone_repo(repo):
                result = False
        return result

    def back_up_repo(self, repo_name):
        """ Back up a given repo on THIS device. """
        with change_working_directory(self.target_dir):
            if not (Path(repo_name).exists() or self.clone_repo(repo_name)):
                return False
            with change_working_directory(repo_name):
                if not self.run_with_indulgence(self.GIT_FETCH):
                    self.git_logger.error(
                        "Problem calling %s for repo: %s",
                        " ".join(self.GIT_FETCH),
                        repo_name
                    )
                    return False
                if not self.run_with_indulgence(self.GIT_PULL):
                    self.git_logger.error(
                        "Problem calling %s for repo: %s",
                        " ".join(self.GIT_PULL),
                        repo_name
                    )
                    return False
        return True

    def back_up_royal_repos(self):
        """ Back up ALL royal repos. """
        result = True
        self.git_logger.info("Backing up royal repos...")
        for repo in self.royal_repos:
            if not self.back_up_repo(repo):
                result = False
        return result

    def schedule_royal_repo_backups(self):
        """ Make sure we back up of royal repos at regular intervals. """
        append_bool = False
        if Path(self.PATH_TO_BASHRC).exists():
            with open(self.PATH_TO_BASHRC, "r") as bashrc:
                if self.BASHRC_ADDITION not in bashrc.read():
                    append_bool = True
            if append_bool:
                with open(self.PATH_TO_BASHRC, "a") as bashrc:
                    bashrc.write("\n"+self.BASHRC_ADDITION)
            return True
        return False

    def install_other_third_party(self):
        """ Install some other useful packages. """
        result = True
        for package in self.OTHER_THIRD_PARTY:
            if not self.install_via_apt(package):
                result = False
        if self.this_platform == "chrome-os":
            for package in self.MISSING_FROM_CHROME:
                if not self.install_via_apt(package):
                    result = False
        return result

    def get_sudo(self):
        """ Get superuser privileges. """
        if self.test_run:
            return
        print("I'm going to need superuser privileges for this...")
        subprocess.run(
            ["sudo", "echo", "Superuser privileges: activate!"], check=True
        )

    def run_apt_with_argument(self, argument):
        """ Run APT with an argument, and tell me how it went. """
        arguments = ["sudo", "apt-get", "--yes", argument]
        result = self.run_with_indulgence(arguments)
        return result

    def update_and_upgrade(self):
        """ Update and upgrade the existing software. """
        self.run_apt_with_argument("update")
        if not self.run_apt_with_argument("upgrade"):
            return False
        if not self.install_via_apt("software-properties-common"):
            return False
        return True

    def install_sqlite(self):
        """ Install both SQLite and a browser for it. """
        if not self.install_via_apt("sqlite"):
            return False
        if not self.install_via_apt("sqlitebrowser"):
            return False
        return True

    def run_essentials(self):
        """ Run those processes which, if they fail, we will have to stop
        the entire program there. """
        for item in self.make_essentials():
            print(item["gerund"]+"...")
            method_to_run = item["method"]
            if not method_to_run():
                self.failure_log.append(item["imperative"])
                return False
        return True

    def run_non_essentials(self):
        """ Run the installation processes. """
        result = True
        for item in self.make_non_essentials():
            print(item["gerund"]+"...")
            method_to_run = item["method"]
            if not method_to_run():
                self.failure_log.append(item["imperative"])
                result = False
        print("Changing wallpaper...")
        if not self.change_wallpaper():
            self.failure_log.append("Change wallpaper")
            # It doesn't matter too much if this fails.
        return result

    def print_outcome(self, passed, with_flying_colours):
        """ Print a list of what failed to the screen. """
        if passed and with_flying_colours:
            print("Installation PASSED with flying colours!")
        elif passed:
            print("Installation PASSED but with non-essential failures.")
        else:
            print("Installation FAILED.")
        if not (passed and with_flying_colours):
            print("\nThe following items failed:\n")
            for item in self.failure_log:
                print("    * "+item)
            print(" ")

    def run(self):
        """ Run the software installer. """
        print("Running His Majesty's Software Installer...")
        self.get_sudo()
        if not self.run_essentials():
            print("\nFinished.\n\n")
            self.print_outcome(False, False)
            return False
        if self.minimal:
            self.print_outcome(True, True)
            return True
        with_flying_colours = self.run_non_essentials()
        print("\nComplete!\n")
        self.print_outcome(True, with_flying_colours)
        return True

####################
# HELPER FUNCTIONS #
####################

@contextlib.contextmanager
def change_working_directory(path):
    """ Changes working directory and returns to previous on exit. """
    prev_cwd = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)

def check_command_exists(command):
    """ Check whether a given command exists on this computer. """
    if shutil.which(command):
        return True
    return False

def create_default_hmss_config_file(path_to):
    """ Create the default HMSS config file. """
    if Path(path_to).exists():
        return
    with open(path_to, "w") as config_file:
        json.dump(
            DEFAULT_HMSS_ARGUMENT_DICT, config_file, indent=CODE_INDENTATION
        )

def make_installer_obj_from_configs(path_to_config_file):
    """ Ronseal. """
    if not Path(path_to_config_file).exists():
        print(
            "No config file found. I'm going to create one for you now at "+
            path_to_config_file
        )
        create_default_hmss_config_file(path_to_config_file)
        print("Please have a look at this file, and then run me again.")
        return False
    with open(path_to_config_file, "r") as config_file:
        attribute_dict = json.load(config_file)
    result = HMSoftwareInstaller()
    for attribute in attribute_dict:
        if hasattr(result, attribute):
            attribute_value = attribute_dict[attribute]
            setattr(result, attribute, attribute_value)
        else:
            warnings.warn("Invalid attribute: "+str(attribute))
    return result

def install_hmss(path_to_config_file=DEFAULT_PATH_TO_HMSS_CONFIG_FILE):
    """ Make the installer object, and then run it. """
    installer_obj = make_installer_obj_from_configs(path_to_config_file)
    if installer_obj:
        installer_obj.run()

def back_up_royal_repos(path_to_config_file=DEFAULT_PATH_TO_HMSS_CONFIG_FILE):
    """ Back up all those repos deemed "royal" on THIS device. """
    installer_obj = make_installer_obj_from_configs(path_to_config_file)
    if installer_obj:
        installer_obj.back_up_royal_repos()
