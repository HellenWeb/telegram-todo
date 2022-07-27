
# Modules

import sqlite3
from datetime import datetime

"""

    Class: "SQLighter"

"""

class SQLighter:
    def __init__(self, db_name):
        self.connect = sqlite3.connect(db_name)
        self.cursor = self.connect.cursor()
    def add_task(self, user_id, name_task):
        with self.connect:
            self.cursor.execute("INSERT INTO `tasks` (`user_id`, `task`, `time`) VALUES (?, ?, ?)", (user_id, name_task, datetime.now().date()))
    def show_tasks(self, user_id):
        with self.connect:
            return self.cursor.execute("SELECT * FROM `tasks` WHERE `user_id` = ?", (user_id,)).fetchall()
    def delete_task(self, user_id, task):
        with self.connect:
            self.cursor.execute("DELETE FROM `tasks` WHERE `user_id` = ? AND `task` = ?", (user_id, task))