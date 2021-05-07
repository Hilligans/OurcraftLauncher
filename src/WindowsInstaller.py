from pathlib import Path
from zipfile import ZipFile
from bs4 import BeautifulSoup
import os

import wget, urllib.request

import SETTINGS
from Installer import Installer

class WindowsInstaller(Installer):

    FAILED = "Failed to install! Exiting..."

    def __init__(self):
        super().__init__(
            {
                "download_java": self.download_java,
                "download_maven": self.download_maven,
                "download_game": self.download_game,
                "compile_game": self.compile_game,
                "run_game": self.run_game
            }
        )

        
    def download_java(self) -> bool:
        try:
            download_path: Path = Path(self.temp_path, SETTINGS.JDK_DOWNLOAD_FILENAME).resolve()
            print("Downloading JDK to: " + str(download_path) + " ...")
            print(wget.download(SETTINGS.WINDOWS_JDK_DOWNLOAD_URL, str(download_path)))
            print("Downloaded JDK to: " + str(download_path))

            print("Extracting JDK to: " + str(self.install_dir) + " ...")
            with ZipFile(download_path) as zipped_file:
                zipped_file: ZipFile
                zipped_file.extractall(self.install_dir)
            print("Extracted JDK to: " + str(self.install_dir))
            print("Installed JDK!")
            return True
        except Exception as e:
            print(e)
            print("Failed to download JDK!")
        return False



    def download_maven(self) -> bool:
        try:
            download_path: Path = Path(self.temp_path, SETTINGS.MAVEN_DOWNLOAD_FILENAME).resolve()
            print("Downloading maven to: " + str(download_path) + " ...")
            print(wget.download(SETTINGS.WINDOWS_MAVEN_DOWNLOAD_URL, str(download_path)))
            print("Downloaded maven to: " + str(download_path))

            print("Extracting maven to: " + str(self.install_dir) + " ...")
            with ZipFile(download_path) as zipped_file:
                zipped_file: ZipFile
                zipped_file.extractall(self.install_dir)
            print("Extracted maven to: " + str(self.install_dir))
            print("Installed maven!")
            return True
        except Exception as e:
            print(e)
            print("Failed to download maven!")
        return False
        


    def download_game(self, version_dir: Path, version: str):
        try:
            download_path: Path = Path(self.temp_path, SETTINGS.GANE_DOWNLOAD_FILENAME).resolve()
            print("Downloading game to: " + str(download_path) + " ...")
            print(wget.download(SETTINGS.GAME_DOWNLOAD_URL, str(download_path)))
            print("Downloaded game to: " + str(download_path))
            install_path: Path = Path(self.installations_dir, version)
            install_path.mkdir(parents=True, exist_ok=True)
            print("Extracting game to: " + str(install_path) + " ...")
            with ZipFile(download_path) as zipped_file:
                zipped_file: ZipFile
                zipped_file.extractall(install_path)
            print("Extracted game to: " + str(install_path))
            return True
        except Exception as e:
            print(e)
            print("Failed to download maven!")
        return False


    def compile_game(self, version_dir: Path, version: str):
        try:
            game_path: Path = Path(version_dir, f"Ourcraft-{SETTINGS.GAME_BRANCH}")
            os.chdir(game_path)
            os.system(f"set JAVA_HOME={self.wrap(Path(self.install_dir, SETTINGS.JDK_DIR))}")
            os.system(self.wrap(Path(self.install_dir, SETTINGS.MAVEN_DIR, "bin", "mvn")) + " package")



            return True
        except Exception as e:
            print(e)
            print("Failed to compile game!")
        return False


    def run_game(self):
        try:
            version = self.get_latest_version()
            version_dir: Path = Path(self.installations_dir, version)
            print("Starting Game!")
            os.system("java -jar " + self.wrap(Path(version_dir, f"Ourcraft-{SETTINGS.GAME_BRANCH}", "target", "Ourcraft-1.0-jar-with-dependencies.jar")))
            return True
        except Exception as e:
            print(e)
            print("Failed to run game!")
        return False



if __name__ == "__main__":
    WindowsInstaller().install()