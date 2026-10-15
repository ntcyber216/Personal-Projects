import sys
import sqlite3
import hashlib
import os
import logging
from datetime import datetime
FIM_DIR = os.path.expanduser("~/.fim")
DB_PATH = os.path.expanduser("~/.fim/fim_data.db")
LOG_PATH = os.path.expanduser("~/.fim/fim.log")

def get_yes_no(question):
  """
  Helper function to request a y/n from the user and validate the input.
  
  Args:
    question = the question to ask the user
  Returns:
    user = the y or n answer from the user
  """
  while True:
    user = input(question)
    if user == "y":
      return True
    elif user == "n":
      return False
    else:
      print("Enter a valid answer.")
        
def get_number(question, min):
  """
  Helper function to request a number from the user and validate the input.
  
  Args:
    question = the question to ask the user
    min = the minimum value allowed, exclusive
  Returns:
    number = the number from the user
  """
  while True:
    try:
      number = int(input(question))
      if number > min:
        return number
      else:
        print("Please enter a greater number. ")
    except ValueError:
      print("Please enter a valid number. ")

def get_file(question):
  """
  Helper function to request a filepath from the user and validate the input.

  Args:
    question = the question you want to ask the user
  Returns:
    filepath = the validated filepath
  """
  while True:
    filepath = input(question)
    if os.path.exists(filepath):
      return filepath
    else:
      print("File path not found.")
  

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
  
  Returns: 
    The user inputted file path and time interval
  """

  filepath = get_file("Enter the file path you wish to monitor. ")
  interval = get_number("Enter the time interval you want to periodically check.", 0) 
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

def setup():
  """
  Sets up the dataase and stores the baseline
  """
  initialize_database()
  filepath, interval = user_config()
    
  connection = sqlite3.connect(DB_PATH)
  cursor = connection.cursor()
  cursor.execute("""
  INSERT INTO config (interval, timestamp, filepath, status) VALUES (?,?,?, ?)
  """, (interval, datetime.now().isoformat(), filepath, "active"))
  connection.commit()
  connection.close()
    
  store_baseline(scan_hash(filepath))
  make_log("INFO", "Baseline stored successfuly.")
  # TODO: Call check function for first integrity check
  # TODO: Register with OS scheduler

def check():
  """
  Scanning function that checks if the baseline hashes agree with the current hashes

  Returns:
    changes = true if changes are detected, false otherwise
  """
  changes = False
  connection = sqlite3.connect(DB_PATH)
  cursor = connection.cursor()
    
  cursor.execute("""
  SELECT filepath FROM config WHERE status = 'active'
  """)
  newfilepath = cursor.fetchone()
  newhash = scan_hash(newfilepath[0])
    
  cursor.execute("""
  SELECT filepath, hash FROM baselines WHERE status = 'active'
  """)
  baseline_dict = dict(cursor.fetchall())

  for filepath, filehash in newhash.items():
    if filepath in baseline_dict:
      if baseline_dict[filepath] != filehash:
        make_log("WARNING", f"{filepath} has been altered.")
        changes = True
    else:
      make_log("WARNING", f"{filepath} has an unexpected file.")
      changes = True

  make_log("INFO", "Scan completed.")
  connection.close()
  return changes

def rebaseline():
  """
  Function that handles the rebaseline process of querying the user and changing the baseline if requested
  """
  connection = sqlite3.connect(DB_PATH)
  cursor = connection.cursor()
    
  if check():
    if get_yes_no("Changes detected, do you wish to establish a new hash? (y/n): "):
      make_log("INFO", "New baseline hash requested.")
      if get_yes_no("Do you wish to establish a new interval? (y/n): "):
        interval = get_number("Enter the interval of time for each check. ", 0)
        make_log("INFO", f"Time interval changed to {interval}")
      else:
        cursor.execute("""
        SELECT interval FROM config WHERE status = 'active'
        """)
        interval = int(cursor.fetchone()[0])
      if get_yes_no("Do you want to monitor a new file path? (y/n): "):
        filepath = get_file("Enter the desired file path: ")
        make_log("INFO", f"Filepath changed to {filepath}")
      else:
        cursor.execute("""
        SELECT filepath FROM config WHERE status = 'active'
        """)
        filepath = cursor.fetchone()[0]
      if get_yes_no("Do you want to erase the original baseline? (y/n): "):
        cursor.execute("""
        DELETE FROM baselines WHERE status = 'active'
        """)
        make_log("INFO", "Baseline deleted")
      else: 
        cursor.execute("""
        UPDATE baselines SET status = 'inactive' WHERE status = 'active'
        """)
        make_log("INFO", "Baseline deactivated")
      cursor.execute("""
      UPDATE config SET status = 'inactive' WHERE status = 'active'
      """)
      cursor.execute("""
      INSERT INTO config (interval, timestamp, filepath, status) VALUES (?,?,?, ?)
      """, (interval, datetime.now().isoformat(), filepath, "active"))
      newhash = scan_hash(filepath)
      store_baseline(newhash)
      make_log("INFO", "New baseline stored successfully")
      check()
  else:
    if get_yes_no("No changes detected, do you still wish to establish a new hash? (y/n): "):
      make_log("INFO", "New baseline hash requested.")
      if get_yes_no("Do you wish to establish a new interval? (y/n): "):
        interval = get_number("Enter the interval of time for each check. ", 0)
        make_log("INFO", f"Time interval changed to {interval}")
      else:
        cursor.execute("""
        SELECT interval FROM config WHERE status = 'active'
        """)
        interval = int(cursor.fetchone()[0])
      if get_yes_no("Do you want to monitor a new file path? (y/n): "):
        filepath = get_file("Enter the desired file path: ")
        make_log("INFO", f"Filepath changed to {filepath}")
      else:
        cursor.execute("""
        SELECT filepath FROM config WHERE status = 'active'
        """)
        filepath = cursor.fetchone()[0]
      if get_yes_no("Do you want to erase the original baseline? (y/n): "):
        cursor.execute("""
        DELETE FROM baselines WHERE status = 'active'
        """)
        make_log("INFO", "Baseline deleted")
      else: 
        cursor.execute("""
        UPDATE baselines SET status = 'inactive' WHERE status = 'active'
        """)
        make_log("INFO", "Baseline deactivated")
      cursor.execute("""
      UPDATE config SET status = 'inactive' WHERE status = 'active'
      """)
      cursor.execute("""
      INSERT INTO config (interval, timestamp, filepath, status) VALUES (?,?,?, ?)
      """, (interval, datetime.now().isoformat(), filepath, "active"))
      newhash = scan_hash(filepath)
      store_baseline(newhash)
      make_log("INFO", "New baseline stored successfully")
      check()
    
  connection.commit()
  connection.close()
  #TODO: Re-register script with OS scheduler 
      
      
    
if __name__ == "__main__":
  setup_log()
  if len(sys.argv) < 2:
    print("Usage: python fim.py --setup | --check | --rebaseline")
  elif sys.argv[1] == "--setup":
    setup()
  elif sys.argv[1] == "--check" or sys.argv[1] == "--scan":
    check()
  elif sys.argv[1] == "--rebaseline":
    rebaseline()
  else:
    print("Usage: python fim.py --setup | --check | --rebaseline")
