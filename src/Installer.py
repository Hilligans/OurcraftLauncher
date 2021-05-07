import pathlib
from pathlib import Path, WindowsPath
from zipfile import ZipFile
from bs4 import BeautifulSoup
import os

import wget, urllib.request

import SETTINGS





class Installer:
    FAILED = "Failed to install! Exiting..."

    def __init__(self, functions: dict):
        self.latest_version = None
        self.functions = functions
        self.install_dir = Path(os.getenv('APPDATA'), SETTINGS.PROJECT_NAME)
        self.installations_dir = Path(self.install_dir, SETTINGS.GAME_VERSIONS_DIR)
        self.temp_path = Path(self.install_dir, SETTINGS.TEMP)
        self.make_paths()


    def make_paths(self):
        self.install_dir.mkdir(parents=True, exist_ok=True)
        self.installations_dir.mkdir(parents=True, exist_ok=True)
        self.temp_path.mkdir(parents=True, exist_ok=True)



    def install(self):
        if not self.install_java():
            print(self.FAILED)
            return
        if not self.install_maven():
            print(self.FAILED)
            return
        if not self.install_game():
            print(self.FAILED)
            return
        if not self.functions['run_game']():
            print(self.FAILED)
            return


    def install_java(self) -> bool:
        # Check if JDK 16 is installed:
        jdk_path: Path = Path(self.install_dir, SETTINGS.JDK_DIR)
        if jdk_path.exists():
            print(f"JDK is installed... ({jdk_path})")
            return True # Already installed ( Hopefully :| )
        
        # Download JDK 16
        x = self.functions['download_java']()
        print(x)
        return x


    def install_maven(self) -> bool:
        # Check if maven is installed:
        maven_path: Path = Path(self.install_dir, SETTINGS.MAVEN_DIR)

        if maven_path.exists():
            print(f"maven is installed... ({maven_path})")
            return True # Already installed ( Hopefully :| )

        # Download maven 3.8.1
        return self.functions['download_maven']()




    def install_game(self) -> bool:
        version = self.get_latest_version()
        version_dir: Path = Path(self.installations_dir, version)
        if version_dir.exists():
            print(f"Latest game version is installed... ({version_dir})")
            return True # Already installed ( Hopefully :| )

        # Download latest version
        if not self.functions['download_game'](version_dir, version):
            return False
        if not self.functions['compile_game'](version_dir, version_dir):
            return False
        return True







    


    def get_latest_version(self) -> str:
        if self.latest_version is None:
            try:
                latest: BeautifulSoup = BeautifulSoup(str(urllib.request.urlopen(SETTINGS.GAME_GITHUB_LINK).read()), 'html.parser')
                self.latest_version = latest.findAll("clipboard-copy", {"class": "BtnGroup-item"})[0]["value"]
            except Exception as e:
                print(e)
                print("Failed to get Latest Version!")
                return
        return self.latest_version


    def wrap(self, path) -> str:
        string = str(path)
        return f'"{string}"' if " " in string else string