# A simple reminder for drinking a sip of water every now and then
from deskdrink.service.notificator import NotificationService
from deskdrink.gui.settingsWindow import MainWindow
from deskdrink.modules.settingsHandler import Settings

from PyQt6.QtWidgets import QApplication, QMenu, QSystemTrayIcon
from PyQt6.QtGui import QAction, QIcon
from importlib import resources

import sys

def main():
    service = NotificationService()
    service.start()

    app = QApplication(sys.argv)

    window = MainWindow()

    settings = Settings()
    trav_icon = resources.files("deskdrink") / (settings._user["icon"] if settings._user["icon"] else settings._default["icon"])

    tray = QSystemTrayIcon()
    with resources.as_file(trav_icon) as iconpath:
        tray.setIcon(QIcon(str(iconpath)))

    menu = QMenu()

    action_settings = QAction("Settings")
    action_quit = QAction("Quit")

    menu.addAction(action_settings)
    menu.addSeparator()
    menu.addAction(action_quit)

    tray.setContextMenu(menu)

    action_settings.triggered.connect(window.show)
    action_quit.triggered.connect(app.quit)

    tray.show()
    # tray.showMessage("Deskdrink", "Service is running")

    app.exec()

if __name__ == "__main__":
    main()

    