# Program to change the settings of the reminder
from PyQt6.QtWidgets import (
    QApplication, 
    QWidget,
    QMainWindow,
    QVBoxLayout,
    QLineEdit,
    QLabel,
    QPushButton
)
from PyQt6.QtGui import QIcon
import sys
from importlib import resources
from deskdrink.modules.settingsHandler import Settings

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self._settings = Settings()

        self.setWindowTitle("Deskdrink Settings")

        self._layout = QVBoxLayout()

        trav_icon = resources.files("deskdrink") / (self._settings._user["icon"] if self._settings._user["icon"] else self._settings._default["icon"])

        with resources.as_file(trav_icon) as iconpath:
            self.setWindowIcon(QIcon(str(iconpath)))
        
        for key in self._settings._default.keys():
            self._layout.addWidget(
                QLabel(
                    objectName=key+"_label", 
                    text=key.title()
                )
            )
            self._layout.addWidget(
                QLineEdit(
                    objectName=(key), 
                    placeholderText=str(self._settings._default[key]),
                    text=(str(self._settings._user[key]) if self._settings._user[key] else "")
                )
            )
            button = QPushButton(
                text=f"Reset {key.title()}"
            )
            button.clicked.connect(
                lambda _, k=key: self.reset(k)
            )
            self._layout.addWidget(button)
        
        button = QPushButton(
                text=f"Save"
        )
        button.clicked.connect(self.save)
        self._layout.addWidget(button)

        button = QPushButton(
                text=f"Reset all"
        )
        button.clicked.connect(lambda: self.reset(None))
        self._layout.addWidget(button)

        widget = QWidget()
        widget.setLayout(self._layout)
        self.setCentralWidget(widget)
    
    def save(self):
        for widget in self.findChildren(QLineEdit):
            self._settings._user[widget.objectName()] = widget.text()
        self._settings.save()

    def reset(self, pSetting):
        if pSetting:
            if not pSetting in self._settings._default.keys():
                return
            self._settings._user[pSetting] = ""
            self.findChild(QLineEdit, pSetting).setText("")
            return
        for k in self._settings._default.keys():
            self._settings._user[k] = ""
        for widget in self.findChildren(QLineEdit):
            widget.setText("")
    
    def closeEvent(self, event):
        event.ignore()
        self.hide()