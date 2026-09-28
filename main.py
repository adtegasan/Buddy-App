import sys

from PySide6.QtWidgets import QApplication

from UI.desktop_pet import DesktopPet


def main():
    app = QApplication(sys.argv)

    window = DesktopPet()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()