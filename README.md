# Personal Diary
This repository contains the implementation for the Personal Diary application. With this application, users are able to create, add to, and customize their own Personal Diary. They can create text entries that are stored onto their machine that can be viewed, edited, or deleted. This version of Personal Diary allows the user to use the application through a command line interface.

- [Container Setup & Teardown](#container-setup--teardown)
- [Using Your Personal Diary](#using-your-personal-diary)
- [Developer Documentation](#developer-documentation)

## Container Setup & Teardown

### Initial Installation

1. Make sure [Docker](https://www.docker.com/get-started/) is installed on your device
2. Build the image
   ```commandline
   docker build -t personal-diary:team_02 -f Dockerfile .
   ```
3. Run the image inside the container
    ```commandline
   docker run --name personal-diary -p 5001:5001 -d personal-diary:team_02
   ```
   
### Accessing the Application

Navigate to [http://127.0.0.1:5001]() in your browser to visit the diary application website.

### Stop and Remove the Container

In order to stop and remove the container, run the following commands
```commandline
docker stop personal-diary
docker rm personal-diary
```

## Using Your Personal Diary
There are currently four operations that the user can perform within their Personal Diary. They can create an entry, view all entries, edit an entry, and delete an entry.

### Creating A Diary Entry
On the command line interface, the user can input the command `python diary_cli.py create` to create a new diary entry.

The user first types in the title of their new diary entry. Then, a text editor will open where the user can type in the body of their new diary entry. Saving the entry on the editor window will successfully create and save the entry. A confirmation is given through the command line interface. Otherwise, the interface will notify the user that nothing was saved.

### Viewing All Diary Entries
On the command line interface, the user can input the command `python diary_cli.py view_all` to view all saved diary entries.

The list will be displayed in descending order of creation. Each entry's ID, date of creation, and title is displayed.

### Reading A Single Diary Entry

On the command line interface, the user can input the command `python diary_cli.py read` to view all information about a specific entry.

A prompt will ask for the user to input the ID assigned to the existing diary entry they wish to view. If no such ID exists, the command fails. 

If the ID does exist, the title, body, date of creation, and time of creation will be displayed.

### Editing A Diary Entry
On the command line interface, the user can input the command `python diary_cli.py edit` to edit a diary entry. 

A prompt will ask for the user to input the ID assigned to the diary entry they wish to edit. If no such ID exists, the command fails. 

If the ID does exist, the user is given the choice to update their title. If no updated title is given, the original title will be passed in. A text editor will open in a new window where the user can make edits to the diary entry. Saving the file will update the entry in the database.

### Deleting A Diary Entry
On the command line interface, the user can input the command `python diary_cli.py delete` to delete a diary entry.

A prompt will ask for the user to input the ID assigned to the existing diary entry they wish to delete. If no such ID exists, the command fails.

If the ID does exist, they must confirm that they want to delete the specified entry by typing "Y" or "N". 

### Help Menu
To access the help menu and commands at any time, type `python diary_cli.py --help` in the command line interface.

## Developer Documentation
The `personal-diary` folder contains the code for the implementation of the Personal Diary. It primarily contains two folders: `personal_diary`, which contains the classes and implementation for the application and `tests`, which contains the unit and feature tests for the implementation. There is also the `requirements.txt` file which lists all libraries used by the application that need to be downloaded.

### personal_diary
Within the `personal_diary` folder is the following:
- `diary.py`: the Python file containing the `Diary` class, representing the Personal Diary. Currently, includes the basic CRUD functions within the diary and functions for reading from and writing to the local database.
- `diary_cli.py`: the Python file containing code for Personal Diary's click command line interface.
- `entry_local_storage.json`: the json file stored locally that saves Personal Diary entry information.
- `app.py`: the Python file containing the initial route setup for a Flask application

### tests
Within the `tests` folder is the following:
- `test_diary.py`: the Python unit test file that tests all functions in the `Diary` class.
- `test_app.py`: the Python integration test file to test Flask REST endpoints
- `test_app_integration.py`: the Python integration test file for diary's CRUD operations

## Team Member Split
### Tania (20%)
- Worked on researching Docker and Dockerizing the application
- Wrote documentation on how to run and install application
- Implemented create_entry operation including how IDs were generated and wrote associated tests 
- Maintained merge requests
### Mausam (20%)
- Researched and set-up Flask base 
- Implemented read_entry operation and wrote associated tests.
- Wrote app integration tests with backend CRUD operations and Flask routes 
### Max (20%)
- Researched and implemented Click command-line interface integration with CRUD operations 
- Tested and debugged Click operations and user interactions through the CLI 
- Implemented delete_entry operation with associated tests
### Danielle (20%)
- Set up and tested CI/CD pipeline yaml file, ensuring that directories and environment variables were set correctly
- Wrote base README (including full instructions on how to use the CLI commands)
### Amarachi (20%)
- Researched Click command-line interface tutorials and starter code
- Implemented update_entry operation with associated tests
- Cleaned up code in create_entry and update_entry