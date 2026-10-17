# File Integrity Monitor

## Overview
This will be a Python-based file integrity monitoring tool to detect any changes within a user specified set of files/directories.

## Design Decisions
To get started with this project, I first wanted to look at the scope of what I was making. To do that, there are a few questions that govern how this will be structured:

Q1: What files does it monitor? A: I want this to be used in a sort of "natural" way, so having it monitor user defined files is best.

Q2: When does it check? A: I do not want this to be a resource drain or a very strict program, so on device startup and user defined intervals.

Q3: What does it do when it finds a change? A: This project is mainly for my learning, so I want it to log any changes to improve my understanding of log analysis.

Q4: What does it store? A: The base hashes and data need to be stored somewhere, and to get more comfortable with SQL I will have the storage within a SQLite database.

Q5: What events should it detect? A: As of the beginning of the project, just modification will do, but if I want to do more later then I will also add file addition and deletion.

Q6: What hashing algorithm should I use? A: The main 2 I even know of are SHA-256 and MD5. MD5 has collision issues so SHA-256 is my best bet for this kind of project. 

## Acknowledgements 
Before we get into the project, I want to clarify that this project is made purely as a learning exercise. For this project I will utilize AI (Claude) to help guide my search and teach me fundamental concepts for me to implement. All code will be written independently by me.
