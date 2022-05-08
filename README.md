# Personal Diary
![coverage](https://cmsc435.garrettvanhoy.com//tarya/personal-diary/badges/main/coverage.svg)

This repository contains the implementation for the Personal Diary application. With this application, users are able to create, add to, and customize their own Personal Diary. They can create text entries that are stored onto their machine that can be viewed, edited, or deleted. This version of Personal Diary allows the user to use the application through a command line interface.

- [Accessing the Diary Web Application](#accessing-the-public-diary-web-application)
- [Running the Project Locally](#running-the-project-locally)
- [Using Your Personal Diary](#using-your-personal-diary)
- [Developer Documentation](#developer-documentation)

## Accessing the Public Diary Web Application 
Navigate to [https://go.umd.edu/diary-app](https://go.umd.edu/diary-app) in your browser to visit the diary application website,
which is deployed in the cloud.

## Running the Project Locally 
The application can also be used locally instead.

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
   
### Accessing the Local Application
Navigate to [http://127.0.0.1:5001](http://127.0.0.1:5001) in your browser to visit the diary application locally.

## Using Your Personal Diary
This section explains some basic core operations that the user can perform within their Personal Diary. They can create an entry, view all entries, edit an entry, and delete an entry. They can also create an account that is used to save and access their entries.

### Creating an Account and Logging In
Upon entering the Personal Diary, the user is first asked to sign in. To first create an account, click the "Sign up" button on the top corner and fill out the fields.
Once the account is created, you can log in using these credentials on the Log In page.

### Viewing All Diary Entries
Upon logging in, the user will see their diary Home Page. On this Home Page is their list of diary entries. The user can select an entry to view, or search for an entry using the search bar.

### Searching Through Entries
In the search bar at the top of the Home Page, the user can search for entries by keyword. Searching will display the specific entries that contain the keyword(s) inputted. Sorting is also possible by using the sort by dropdown.

### Creating A Diary Entry
The user can create a new diary entry by pressing the Create Entry button in the bottom right corner of the Home Page. The user can then create a new entry by giving it a title and contents with tags or an indicated mood. Entry appearance can be customized like by changing the text color.
Press the Save button to store the entry once finished.

### Reading A Single Diary Entry
The user can select a diary entry among the saved entries from the Home Page. Clicking an entry's title will take you to its page to view.

### Editing A Diary Entry
The user can select an entry then edit it by clicking the Edit button. Both the title and contents can be edited. There is also a text editor for editing entries with similar customization options as creating.

### Deleting A Diary Entry
To delete an entry, select it from the Home Page and click the red Delete button. A message at the top of the Home Page will confirm that the entry has been permanently deleted. 

## Developer Documentation
The `personal-diary` folder contains the code for the implementation of the Personal Diary. It primarily contains two folders: `personal_diary`, which contains the classes and implementation for the application and `tests`, which contains the unit and feature tests for the implementation. There is also the `requirements.txt` file which lists all libraries used by the application that need to be downloaded.

### personal_diary
Within the `personal_diary` folder is the following:
- `app.py`: the Python file containing code for Personal Diary's Flask app.
- `diary.py`: the Python file containing the `Diary` class, representing the Personal Diary. Currently, includes the basic CRUD functions within the diary and functions for reading from and writing to the local database.
- `diary_user.py`: the Python file containing the class with helper functions related to creating, reading, updating, and deleting a diary user.
- `forms.py`: the Python file with code for the form used for user to add a new entry to the diary by inputting a title and body.
- `models.py`: the Python file with code for the data model of the diary entries.
- `personal-diary/templates`: This folder contains html files that are used as templates for the pages used in the Flask app.
- `personal-diary/static`: This folder contains the custom build of CKEditor used for the Personal Diary's text fields and the style.css file to style the appearance of pages.

### tests
Within the `tests` folder is the following:
- `test_diary.py`: the Python unit test file that tests all functions in the `Diary` class.
- `test_app.py`: the Python integration test file to test Flask REST endpoints.
- `test_diary_integration.py`: the Python integration test file for the diary's operations.
- `test_diary_user.py`: the Python test suite for user-related operations.

### Sphinx Documentation
The `docs` folder contains the project's automatically-generated Sphinx documentation. To access the Sphinx documentation,
open on the `index.html` file in a browser. This will open the main page that links to the specific module pages.

## Team Member Split
### Tania (20%)
- Updated UI for Sign Up and Login page
- Made updates to UI for all pages
- Updated tests to increase code coverage
- Implemented option to delete user
- Refactored organization of app

### Mausam (20%)
- Updated UI for read entry page
- Implemented addition of mood option to diary entries
- Deployed app to cloud to be accessible from IP address and updated documentation

### Max (20%)
- Updated UI for Home page
- Implemented sort functionality and updated tests involving it
- Updated comments and added code coverage badge to readme

### Danielle (20%)
- Generated Sphinx documentation
- Implemented password confirmation during signup
- Updated user’s name to appear on homepage navbar
- Added implementation to allow users to attach images to entry

### Amarachi (20%)
- Implemented daily reminder notifications to create an entry and wrote associated tests
