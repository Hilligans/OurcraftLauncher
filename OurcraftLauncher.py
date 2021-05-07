import platform
from WindowsInstaller import WindowsInstaller


def main() -> None:

    operating_system: str = platform.system()

    if operating_system == "Windows":
        WindowsInstaller().install()
    else:
        print("Your Operating system is not currently supported! Check back soon.")
    return 

if __name__ == '__main__':
    main()
