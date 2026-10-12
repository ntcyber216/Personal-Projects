import sqlite3
import hashlib
import os
import logging

FIM_DIR = os.path.expanduser("~/.fim")
DB_PATH = os.path.expanduser("~/.fim/fim_data.db")

def initialize_database():
  """Creates the  ~/.fim directory and fim_data.db database while creating the 3 tables we will be storing data in within SQLite"""
  os.makedirs(FIM_DIR, exist_ok = True)
  connection = sqlite3.connect(DB_PATH)
  cursor = connection.cursor()
  cursor.execute("""
  CREATE TABLE IF NOT EXISTS baselines (
  id INTEGER PRIMARY KEY,
  filepath TEXT,
  hash TEXT,
  timestamp TEXT,
  status TEXT
  )
  """)
  cursor.execute("""
  CREATE TABLE IF NOT EXISTS logs (
  id INTEGER PRIMARY KEY,
  timestamp TEXT,
  message TEXT,
  event TEXT)
  """)
  cursor.execute("""
  CREATE TABLE IF NOT EXISTS config (
  id INTEGER PRIMARY KEY,
  interval INTEGER,
  timestamp TEXT,
  filepath TEXT, 
  status TEXT )
  """)
  connection.commit()
  connection.close()



if __name__ == "__main__":
    pass
