import pymysql
import re
import sys


class SqlHandler:
    db = None
    cursor = None
    text = ''

    def __init__(self, config, database):
        pattern = re.compile(r"sql://(.+):(.+)@((?:\d{1,3}\.){3}\d{1,3}):(\d+)\s*")
        configFile = open(config, mode='r')
        c = configFile.readline()
        configFile.close()
        match = pattern.match(c)
        if not match:
            raise Exception(r"Invalid SQL URL. Expect sql://name:passwd@ip:port")
        self.db = pymysql.connect(match.group(3), match.group(1), match.group(2), database)
        self.db.autocommit(True)
        self.cursor = self.db.cursor()
        self.text = match.group(0)

    def execute(self, command, *args):
        try:
            self.cursor.execute(command, args)
            self.db.commit()
        except:
            self.db.ping()
            self.cursor = self.db.cursor()
            self.cursor.execute(command, args)
            self.db.commit()

    def continuous_exec(self, command, *args):
        try:
            self.cursor.execute(command, args)
        except:
            self.db.ping()
            self.cursor = self.db.cursor()
            self.cursor.execute(command, args)

    def commit(self):
        self.db.commit()

    def select(self, command, *args):
        # if args == ():
        #     self.cursor.execute(command)
        # else:
        try:
            self.cursor.execute(command, args)
            return self.cursor.fetchall()
        except:
            self.db.ping()
            self.cursor = self.db.cursor()
            self.cursor.execute(command, args)
            return self.cursor.fetchall()

    def __del__(self):
        self.db.close()
