import subprocess
import os
import platform
import time
from zipfile import ZipFile
import ctypes
import shutil
from urllib.request import urlopen


operatingSystem = ""
latestProject = ""
projectName = ""
pathToProject = ""

javaName = "jdk-16"


def installWindows():
    if not os.path.exists(pathToProject):
        os.mkdir(pathToProject)
    if not os.path.exists(pathToProject + "\\jdk-16"):
        print("downloading java")
        os.system('curl -L https://download.java.net/java/GA/jdk16/7863447f0ab643c585b9bdebf67c69db/36/GPL/openjdk-16_windows-x64_bin.zip --output java16.zip --silent')
        with ZipFile("java16.zip") as zip:
            zip.extractall(pathToProject)
            zip.close()
        os.remove("java16.zip")
    if os.getenv("JAVA_HOME") is None:
        os.system("setx JAVA_HOME \"" + pathToProject + "\\" + javaName + "\"")
    time.sleep(2)
    try:
        subprocess.check_output(['WHERE', 'mvn'])
    except:
        if not os.path.isfile('C:\\Program Files\\Maven\\apache-maven-3.8.1\\bin\\mvn.cmd'):
            print("downloading maven")
            os.system('curl -L https://mirror.its.dal.ca/apache/maven/maven-3/3.8.1/binaries/apache-maven-3.8.1-bin.zip --output maven.zip --silent')
            with ZipFile("maven.zip") as zip:
                os.mkdir(pathToProject + '\\Maven')
                zip.extractall(pathToProject + '\\Maven')
                zip.close()
                os.remove("maven.zip")
            os.system('setx path "%path%;' + pathToProject + '\\Maven\\apache-maven-3.8.1\\bin"')
            time.sleep(2)
        else:
            os.system('setx path "%path%;C:\\Program Files\\Maven\\apache-maven-3.8.1\\bin" /M')
            time.sleep(2)

    if not os.path.exists(pathToProject + "\\Ourcraft-" + projectName + ".jar"):
        print("downloading game")
        os.system('curl -L https://github.com/Hilligans/Ourcraft/archive/refs/heads/main.zip --output ourcraft.zip --silent')
        with ZipFile("ourcraft.zip") as zip:
            zip.extractall(pathToProject)
            zip.close()
            os.remove("ourcraft.zip")
        os.chdir(pathToProject + "\\Ourcraft-main")
        time.sleep(2)
        os.system("mvn package")
        os.rename(pathToProject + "\\Ourcraft-main\\target\\Ourcraft-1.0-jar-with-dependencies.jar", pathToProject + "\\Ourcraft-" + projectName + ".jar")
        try:
            shutil.rmtree(pathToProject + "\\Ourcraft-main")
        except:
            a = ""


def launchGame():
    print("starting game")
    os.chdir(pathToProject + "\\jdk-16\\bin")
    os.system("java -jar \"" + pathToProject + "\\Ourcraft-" + projectName + ".jar\"")


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if __name__ == '__main__':
    operatingSystem = platform.system()
    latestProject = str(urlopen("https://github.com/Hilligans/Ourcraft/commits/main").read())
    pathToProject = os.getenv('APPDATA') + "\\Ourcraft"
    start = latestProject.index("datetime") + 10
    for x in range(0, 50):
        if latestProject[start + x] == '"':
            break
        if latestProject[start + x] == ":":
            continue
        projectName += latestProject[start + x]
    if operatingSystem == "Windows":
        installWindows()
    launchGame()

