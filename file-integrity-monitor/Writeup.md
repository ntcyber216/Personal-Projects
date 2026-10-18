# Overview
What is this file here for if I already have the README? Well, I realized that I wanted to document a little more detail about my learning process and what I had to do to get this project working, but far fewer people are interested in that than just the functionality of this project, so I separated it from the README. This means those people can go read that for project design decisions and implementations while this part is mostly just for myself and journaling purposes.

## Motivations
Why did I want to do this? To start, I recently acquired my CompTIA Security+ Certification, but my experience with personal projects was rather limited. There were many things I learned about while studying that gave me ideas for projects: Intrusion Detection Systems, Intrusion Prevention Systems, File Integrity Monitors, DNS Sinkholes, DHCP, Firewall rules, Access control, maybe even simulating a RADIUS interaction, but FIM seemed like a great way to both refresh my rusty Python skills and get my first working cybersecurity related application. As a bonus, I also get to learn how to use Github to store all of my future projects.

## Previous Experience
This is far from my first time coding, and I wanted to have this section here to outline what knowledge I knew before actually starting this process. I have taken multiple computer science classes in high school, my first being AP Computer Science A where I ended up getting the highest score on the final exam. Learning Java first was a great first step into coding, because when I took a Python course, the fundamentals of Java sort of "over-prepared" me for Python. Not to say Python is easy by any means, but at my level it is significantly less work compared to Java with its lighter syntax. Unfortunately after these classes I stopped coding as nearly as much, so a few years went by with little practice until now. This is not to say I forgot everything, in fact, after practicing a bit of Python I felt mostly back to where I was, but my logical reasoning and problem solving with code is still a bit rusty. To add on, I had done very little work with SQL. For one of my college courses I had a project to do in MySQL, but it had nothing to do with using SQL and Python in tandem. In a bit of a higher level sense, my Sec+ knowledge introduced me to the idea of this project and I knew what a FIM had to do, but other than that I was going to have to learn quite a bit to get started. 

## Initial Design Decisions
I intentionally made decisions about what this project would look like based upon if I would learn by doing it. This is why I decided to use sqlite3 over a JSON file. SQL was something I saw come up numerous times when searching for the top requested skills in cybersecurity, so having a project that required me to use SQL helped me to get a baseline knowledge before moving on to more advanced things. Additionally, I wanted to use SHA-256 as a hashing algorithm because it came up multiple times while studying for Sec+, so it seemed like a natural extension of that. Furthermore, I wanted more work with operating systems, which is why I used the OS library for this project as well. 

## SQLite3
If I wanted to do anything with a database this is the library I landed on using (and what Claude suggested). If you have not seen the acknowledgement section in the README, I used Claude as a tutor to explain concepts and then let me figure out on my own how to implement them. Just to be clear, this project is still done by me, with my own original work. The AI involvement is purely for educational purposes. Continuing on, I had to learn some of the essential functions that I will need to get this working.
```python
connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS baselines (
id INTEGER PRIMARY KEY,
filepath TEXT,
hash TEXT,
timestamp TEXT,
status TEXT)
""")
#...rest of the tables I need to create

connection.commit()
connection.close()
```
I think it would be easier to explain what I had to learn if I showed a section containing a majority of the sqlite functions I ended up using, as well as showing the SQL itself. Learning these basic functions of sqlite3 was actually pretty easy for me. Weirdly enough it reminded me of my time in my Video Game Programming class where we used the Monogame library in C#. A few basic concepts applied here, like connecting to the file and even having to close the connection. Sqlite3.connect was most similar to the SpriteBatch functions where you had to use Content.Load<Texture2D>("file_here") to connect to the file and even the .close() was like how you had to use .end() when you are finished drawing. Anyways, after learning the basic functions of connect(), cursor(), commit() and close(), I then had to learn some more SQL commands. This too was pretty easy, to me it even reads out like a broken English. In the section above, I am making the baselines table and the SQL literally reads like "Create a table if it does not already exist called baselines."

## Python Libraries:

### OS
As of writing this section, I have not utilized the OS library to register the script to run at the user defined intervals. For now, the main uses for the os library are here:
```python
FIM_DIR = os.path.expanduser("~/.fim")
DB_PATH = os.path.expanduser("~/.fim/fim_data.db")
LOG_PATH = os.path.expanduser("~/.fim/fim.log")
```
And here: 
```python
os.makedirs(FIM_DIR, exist_ok = True)
```
The os library is a lot more intuitive than I thought. After reading through the documentation and example uses, I mostly understood how to use the os library pretty quickly. 

### Hash Lib
Here is the section of code where I utilized hashing:
```python
hashes = {}
for root, dirs, files in os.walk(filepath, topdown = False):
  for name in files:
    h = hashlib.new('sha256')
    with open(os.path.join(root,name), 'rb') as f:
      content = f.read()
      h.update(content)
      hashes[os.path.join(root,name)] = h.hexdigest()
return hashes
```
It is a pretty light implementation, but before this I had not worked with either hashlib or opening files in Python. After only a bit of research, hashlib is pretty simple to use. In this section I had more difficulty getting the for loop to properly work with os.walk because for loops in python were a bit harder for me to understand than Java. In that sense Java's complexity serves to benefit because being able to write in such a detailed way makes it easier to interpret for me, but after a bit research and example bits of code in the documentation I was able to figure it out. Another thing I had to utilize here that I did not know fully before was dictionaries. Looking it up I found that it was very similar to hash maps from Java where a data entry is linked to a key. From there I just needed the syntax and to put it all together. 

## Issues
There were multiple hiccups and errors that needed to be resolved during development. Aside from the usual typos or syntax issues, I found myself having to go back to refactor my code often. When writing the code that requires user input (which was towards the end of the development), I got too irritated by the amount of input validation so I decided to create helper functions. This meant that to make things uniform, I had to go back to code I wrote days ago to make them use the new helper functions. Furthermore, my code itself is far from perfect. As much as I would like to go back to optimize the whole thing completely, for the purposes of my learning it really would not do much for me. I already refactored a few of the functions, but as I see it my time is better spent starting a new project and being more conscious of optimization. The most glaring optimization issue with this code is the rebaseline method. By that point I had already refactored previous functions over 3 different times to accommodate the helper functions I designed only for this function, so I wanted to finish quickly. For context, the rebaseline method is intended to create a new hash dictionary if a change was detected and prompt the user for details. It is intended to go through with its process if a change is detected and the user wants to or if no change is detected and the user wants to anyways. This means I basically have to write it twice for each case, so I just took the lazy way and copy pasted. Looking back I am sure there is a better way to do it, but I would not learn as much from spending time on it. I know writing efficient code is nearly as important as it working, but this is a personal project rather than a fleshed out security tool. 

## Errors

### FileNotFoundError
Continuing on, aside from having to update my Python version from 3.9 to 3.11 to get some code to work, there were 2 major bugs. The first was with this function: 
```python
LOG_PATH = os.path.expanduser("~/.fim/fim.log")
def setup_log():
  logging.basicConfig(
    filename = LOG_PATH,
    level = logging.INFO,
    format = '%(asctime)s | %(levelname)s | %(message)s'
  )

if __name__ == "__main__":
  setup_log()
```
This bug was a rather difficult one to spot, but the issue was the setup_log is the first function that runs, but it creates a log file without /.fim being created yet which causes a FileNotFoundError. That happens later with this line in the initialize_database function:
```python
os.makedirs(FIM_DIR, exist_ok=True)
```
This error happened simply because I wrote initialize_database before the setup_log function, so I was not thinking retroactively when writing the setup_log function. The fix was just to add that line into the setup_log function so it both makes the directory and adds the log file rather than the directory being made later. 

### Database Locked
To me, this was the more interesting of the 2 errors despite its simple origin. Whenever a log entry needs to be added into the table, this function is called:
```python
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
```
And this is what the section of the check function causing the error looked like
```python
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
# Irrelevant code to the error...
connection.close()
```
The issue here is that the connection to the database is open for way too long. This means that the connection is open while make_log proceeds to then open its own connection. Only one connection is allowed at a time so the database locks itself and causes an error. This fix involved a bit of refactoring, but I just made it so any connection closes itself as soon as possible to prevent conflict.

## Vulnerabilities
This is where my Sec+ studying comes to practical use. The section of code I want to highlight is this:
```python
cursor.execute("""
INSERT INTO baselines (filepath, hash, timestamp, status) VALUES (?,?,?,?)
""", (filepath, file_hash, datetime.now().isoformat(), "active"))
```
When I initially started writing, it looked like this:
```python
cursor.execute("""
INSERT INTO baselines (filepath, hash, timestamp, status) VALUES (filepath, file_hash, datetime.now, "active")
""")
```
If you know the basics about using SQL in Python this is a very big red flag for an SQL injection, as the variable named filepath is a user defined string. This means that if the user entered sql code in when prompted, it would execute the code into the database. I learned about how SQL injections worked in Sec+, but I have never actually seen the mechanics of what happens in the code. The fix for this was to instead use this (?,?,?,?) part where instead of passing the values directly it sort of inserts the values into that question mark block as a tuple, meaning it reads any malicious code as a string rather than executable code.

## Going forward
There's plenty of minor issues with this project, and I haven't fully added the OS scheduler part yet, but I think I will leave that to future me. For now, I am happy with how this project turned out. It completes its core function and also helped me learn a lot about using python for cybersecurity. One day I may come back to this if I feel like it, but for now this will be my first finished github project of many more to come.
