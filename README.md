# Personal Diary
This repository contains the implementation for the Personal Diary application. With this application, users are able to create, add to, and customize their own Personal Diary. They can create text entries that are stored onto their machine that can be viewed, edited, or deleted. This version of Personal Diary allows the user to use the application through a command line interface.

## Installation
(steps/information about downloading through docker?)

## Using Your Personal Diary
There are currently four operations that the user can perform within their Personal Diary. They can create an entry, view all entries, edit an entry, and delete an entry.

### Creating A Diary Entry
On the command line interface, the user can input the command `python diary_interface.py create` to create a new diary entry.

The user first types in the title of their new diary entry. Then, a new window will open a text editor where the user can typed in the body of their new diary entry. Saving the entry on the editor window will successfully create and save the entry. A confirmation is given through the command line interface. Otherwise, the interface will notify the user that nothing was saved.

### Viewing All Diary Entries
On the command line interface, the user can input the command `python diary_interface.py view_all` to view all saved diary entries.

The list will be displayed by ID in descending order. Each entry's ID, date of creation, and title is displayed.

### Editing A Diary Entry
On the command line interface, the user can input the command `python diary_interface.py edit` to edit a diary entry. 

A prompt will ask for the user to input the integer ID assigned to the diary entry they wish to edit. First, the user given the choice to update their title. If no updated title is given, the orginal title will be passed in. A text editor will open in a new window where the user can make edits to the diary enty. Saving the file will update the entry in the database.

### Deleting A Diary Entry
On the command line interface, the user can input the command `python diary_interface.py delete` to delete a diary entry.

A prompt will ask for the user to input the integer ID assigned to the existing diary entry they wish to delete. They must confirm that they want to delete the specified entry by typing "Y" or "N". If not such id exists, the command fails.

### Help Menu
When the user first opens the command line interface, they are show a menu with the different Personal Diary commands and their descriptions. 

To access the help menu and commands at any time, type `python diary_interface.py --help` in the command line interface.

## Developer Documentation
The `personal-diary` folder contains the code for the implementation of the Personal Diary. It primarily contains two folders: `personal_diary`, which contains the classes and implementation for the application and `tests`, which contains the unit and feature tests for the implementation. There is also the `requirements.txt` file which lists all libraries used by the application that need to be downloaded.

### personal_diary
Within the `personal_diary` folder is the following:
- `diary.py`: the python file containing the `Diary` class, representing the Personal Diary. Currently includes the basic CRUD functions within the diary and functions for reading and writing the local database.
- `diary_interface.py`: the python file containing code for Personal Diary's click command line interface.
- `entry_local_storage.json`: the json file stored locally that saves Personal Diary entry information.

### tests
Within the `tests` folder is the following:
- `test_diary.py`: the python unit test file tests all functions in the `Diary` class.
