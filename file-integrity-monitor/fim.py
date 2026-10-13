import sqlite3
import hashlib
import os
import logging
from datetime import datetime
FIM_DIR = os.path.expanduser("~/.fim")
DB_PATH = os.path.expanduser("~/.fim/fim_data.db")
LOG_PATH = os.path.expanduser("~/.fim/fim.log")

def initialize_database():
  """
  Creates the  ~/.fim directory and fim_data.db database while creating the 3 tables we will be storing data in within SQLite
  """
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

def user_config():
  """
  Sets up the user inputs and configurations for the file path and interval
  Returns: the user inputted file path and time interval
  """
  while True:
    filepath = input("Enter the file path you wish to monitor. ")
    if os.path.exists(filepath):
      break
    else:
      print("File path not found.")
    
  while True:
    try:
      interval = int(input("Enter the interval of time for each check: "))
      if interval > 0:
        break
      else:
        print("Please enter a positive number.")
    except ValueError:
      print("Please enter a valid number")
  return filepath, interval

def scan_hash(filepath):
  """
  Scans each file recursively within the specified file path
  
  Args:
    filepath = the directory path to recursively scan each file

  Returns:
  A dictionary linking the file path to its respective hash
  """
  hashes = {}
  for root, dirs, files in os.walk(filepath, topdown = False):
    for name in files:
      h = hashlib.new('sha256')
      with open(os.path.join(root,name), 'rb') as f:
        content = f.read()
        h.update(content)
      hashes[os.path.join(root,name)] = h.hexdigest()
  return hashes

def store_baseline(hashes):
  """
  Connects to the SQLite database to add the hashes directory into the tables

  Args:
    Hashes: A dictionary containing each file's path and its respective hash
  """
  connection = sqlite3.connect(DB_PATH)
  cursor = connection.cursor()

  for filepath, file_hash in hashes.items():
    cursor.execute("""
    INSERT INTO baselines (filepath, hash, timestamp, status) VALUES (?,?,?,?)
    """, (filepath, file_hash, datetime.now().isoformat(), "active"))
  connection.commit()
  connection.close()

  def setup_log():
    """
    Sets up the python logging library to add the logs in the format: time | level | message
    """
    logging.basicConfig(
      filename = LOG_PATH,
      level = logging.INFO,
      format = '%(asctime)s | %(levelname)s | %(message)s'
    )
    
  def make_log(event_type, message):
    """
    Reusable function to add the log both into the log file and log table in SQLite
    """
    match event_type:
      case "WARNING":
        logging.warning(message)
      case "ERROR":
        logging.error(message)
      case _:
        logging.info(message)
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("""
    INSERT INTO logs (timestamp, message, event) VALUES (?,?,?)
    """, (datetime.now().isoformat(), message, event_type))
    connection.commit()
    connection.close()
    



if __name__ == "__main__":
  setup_log()
  pass
