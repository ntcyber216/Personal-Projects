## SETUP

Ask user what file path to monitor

Ask user what time interval the program should assess the files

Verify that the file path exists and user input is valid

Scan all files in the path (recursively for all subfiles) + Utilize SHA-256 to hash each file

Store baseline hash in SQLite

Log the completion of the setup process

Run first integrity check

Log the results of the first scan

Register script with OS scheduler at the user’s defined interval

## CHECK

Access the SQLite database to acquire the user defined filepath

Scan the files recursively and hash each one

Access the SQLite database to get every baseline hash

Compare baseline hash to scanned hash, in the case of file addition and deletion, log and continue

Log any discrepancy and scan completion

Exit

## RE-BASELINE

If changes are detected, notify user and prompt them to accept or deny the new baseline, if the user wishes to re-baseline anyways, continue

If accepted, continue and prompt user to keep old time interval, or establish a new one. Additionally, prompt user to keep old file path or define a new one. If denied, exit now.

Log user action and any interval changes

Prompt user if original baseline should be deleted, leave it in the SQLite database if not and tag the data as inactive, erase if yes

Log user action and deletion (if requested)

Scan the new files recursively and hash each file

Store new baseline hashes in SQLite

Log the completion of the setup process

Run new integrity check

Log the results of the integrity check

Re-Register script with OS scheduler if user has defined a new interval, and delete the old one if so
