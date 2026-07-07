# This Module shows a drink notification, if it is run
from deskdrink.modules.settingsHandler import Settings
from PyQt6.QtCore import QThread
from notifypy import Notify
from importlib import resources
import json
# import asyncio

class NotificationService(QThread):
    def __init__(self):
        super().__init__()
        self._settings = Settings()
        self._interval = 0
        self._update_available = False
        self._is_running = True
    
    def run(self):
        print("Notifications scheduled.")
        self.notify("Deskdrink service started", "You'll receive reminders for drinking something.")
        while self._is_running:
            self.autoupdate()
            for _ in range(self._interval):
                QThread.sleep(1)
            self.notify(self.getConfig("title"), self.getConfig("message"))
            print("Notification sent.")
        print("Notifications stopped.")

    # Trigger service stop
    def stop(self):
        self._is_running = False

    # Trigger service update
    def update(self):
        self._update_available = True

    # Update configuration internally
    def autoupdate(self):
        # print("Updating Notifications...")
        
        self._settings.load()
        self.setInterval()
        self._update_available = False
        
        # print("Updated.")

    # Send notification using configuration
    def notify(self, title, message):
        notification = Notify()

        notification.title = title
        notification.message = message

        audio = self.getConfig("audio")
        if not audio == "" and not audio == "none":
            notification.audio = resources.files("deskdrink") / audio if "audios/" in audio else audio
        icon = self.getConfig("icon")
        if not icon == "" and not icon == "none":
            notification.icon = resources.files("deskdrink") / icon if "icons/" in icon else icon
        
        notification.send()

    # Read configuration parameters
    def getConfig(self, item):
        return self._settings._user[item] if self._settings._user[item] else self._settings._default[item]
    
    def setInterval(self):
        self._interval = int(self.getConfig("interval"))*60