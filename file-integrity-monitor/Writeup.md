# Overview
What is this file here for if I already have the README? Well, I realized that I wanted to document a little more detail about my learning process and what I had to do to get this project working, but far fewer people are interested in that than the just the functionality of this project, so I separated it from the README. This means those people can go read that for project design decisions and implementations while this part is mostly just for myself and journaling purposes.

## Motivations
Why did I want to do this? To start, I recently acquired my CompTIA Security+ Certification, but my experience with personal projects was rather limited. There were many things I learned about while studying that gave me ideas for projects: Intrusion Detection Systems, Intrusion Prevention Systems, File Integrity Monitors, DNS Sinkholes, DHCP, Firewall rules, Access control, maybe even simulating a RADIUS interaction, but FIM seemed like a great way to both refresh my rusty Python skills and get my first working cybersecurity related application. As a bonus, I also get to learn how to use Github to store all of my future projects.

## Previous Experience
This is far from my first time coding, and I wanted to have this section here to outline what knowledge I knew before actually starting this process. I have taken multiple computer science classes in high school, my first being AP Computer Science A where I ended up getting the highest score on the final exam. Learning Java first was a great first step into coding, because when I took a Python course, the fundamentals of Java sort of "over-prepared" me for Python. Not to say Python is easy by any means, but at my level it is significantly less work compared to Java with its lighter syntax. Unfortunately after these classes I stopped coding as nearly as much, so a few years went by with little practice until now. This is not to say I forgot everything, in fact, after practicing a bit of Python I felt mostly back to where I was, but my logical reasoning and problem solving with code is still a bit rusty. To add on, I had done very little work with SQL. For one of my college courses I had a project to do in MySQL, but it had nothing to do with using SQL and Python in tandem. In a bit of a higher level sense, my Sec+ knowledge introduced me to the idea of this project and I knew what a FIM had to do, but other than that I was going to have to learn quite a bit to get started. 

## SQLite3
SQLite3 or sqlite3? Anyways, if I wanted to do anything with a database this is the library I landed on using (and what Claude suggested). If you have not seen the acknowledgement section in the README, I used Claude as a tutor to explain concepts and then let me figure out on my own how to implement them. Just to be clear, this project is still done by me, with my own original work. The AI involvement is purely for educational purposes. Continuing on, I had to learn some of the essential functions that I will need to get this working.
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
I think it would be easier to explain what I had to learn if I showed a section containing a majority of the sqlite functions I ended up using, as well as showing the SQL itself. Learning these basic functions of sqlite3 was actually pretty easy for me. Weirdly enough it reminded me of my time in my Video Game Programming class where we used the Monogame library in C#. A few basic concepts applied here, like connecting to the file and even having to close the connection. Sqlite3.connect was most similar to the SpriteBatch functions where you had to use Content.Load<Texture2D>("file_here") to connect to the file and even the .close() was like how you had to use .end() when you are finished drawing. Anyways, after learning the basic functions of connect(), cursor(), commit() and close(), I then had to learn some more SQL commands. This too was pretty easy, to me it even reads out like a broken English. In this section, I am making the baselines table and the SQL literally reads like "Create a table if it does not already exist called baselines."
```python
cursor.execute("""
SELECT filepath FROM config WHERE status = 'active'
""")
cursor.execute("""
UPDATE config SET status = 'inactive' WHERE status = 'active'
""")
cursor.execute("""
INSERT INTO baselines (filepath, hash, timestamp, status) VALUES (?,?,?,?)
""", (filepath, file_hash, datetime.now().isoformat(), "active"))
```
Here is some of the other SQL keywords I learned how to use, once you learn the keywords its like writing just plain English. The important thing I wanted to highlight here was that last bit. 
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
It is a pretty light implementation, but before this I had not worked with both hashlib or opening files in Python. After only a bit of research, hashlib is pretty simple to use. In this section I had more difficulty getting the for loop to properly work with os.walk because for loops in python were a bit harder for me to understand than Java. In that sense Java's complexity serves to benefit because being able to write in such a detailed way makes it easier to interpret for me, but after a bit research and example bits of code in the documentation I was able to figure it out. Another thing I had to utilize here that I did not know fully before was directories. Looking it up I found that it was very similar to hash maps from Java where a data entry is linked to a key. From there I just needed the syntax and it was intuitive to utilize. 
