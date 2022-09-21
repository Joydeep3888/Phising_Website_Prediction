import logging as lg
from datetime import datetime

class logger:
    def __init__(self):
        pass
    def apply_log(self, file_name, msg):
        self.now = datetime.now()
        self.date = self.now.date()
        self.current_time = self.now.strftime("%H:%M:%S")
        file_name.write(str(self.date) + "/" + str(self.current_time) + "\t\t" + msg + "\n")