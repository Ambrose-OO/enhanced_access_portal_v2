# enhanced_access_portal_v2

## Running on local host

### 1. Git clone the repository

Clone this repository to your local machine system files using the following clone link:
```https://github.com/Ambrose-OO/enhanced_access_portal_v2```

For further details on how to do this, read: 
```https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository```

### 2. Setup Visual Studio Code or another IDE

For this step you want to setup Visual Studio Code (VSC) or another IDE that can run and edit python scripts.

To setup VSC, read:
```https://code.visualstudio.com/docs/getstarted/getting-started```

To setup VSC with Python, read: 
```https://www.youtube.com/watch?v=D2cwvpJSBX4```

The IEAP has been developed with Python v3.9.0 64-bit. If your installation of python doesn't run well, try to use the same version as detailed. 

The youtube video provided also covers the python PIP installation manager.

### 3. Install the django package

Access pip on the terminal as detailed in the youtube video in step 2. And install this version of django:
```3.1.5```

This should give you the django library and dependencies that come with it to launch django.

### 4. Settings

In VSC, check the settings script in this path: ```enhanced_access_portal/enhanced_access_portal/settings.py```, and ensure line 28 equates to:
```ALLOWED_HOSTS = []```

### 5. Reverting changes to database and user sessions

To revert back changes made to the database and user sessions use version control after cloning the repository, you can enable version controlling with Git/Github on VSC to revert changes to the ```db.sqlite3``` file. Follow the documentation here: ```https://code.visualstudio.com/docs/introvideos/versioncontrol```

### 6. Running the local host

On your terminal in VSC, direct yourself to ```enhanced_access_portal/enhanced_access_portal``` using the command ```cd enhanced_access_portal```

Assistance with commands on terminal can be read on here: ```https://tutorials.codebar.io/command-line/introduction/tutorial.html#:~:text=The%20cd%20command%20allows%20you,command%20is%20cd%20your%2Ddirectory%20.&text=Now%20that%20we%20moved%20to,changed%20into%20a%20new%20directory.```

Then run the following command: 
```python manage.py runserver```

Ensuring that python is part of your systems path.

This as a result should create a local host on your machine.

### 7. Connecting to the local host website

To connect to the local host website, open a web browser on your machine such as Google chrome and search: 
```http://127.0.0.1:8000/login_page/``` 

From here you can login using credentials stored in the ```db.sqlite3`` file part of the project. Which can be viewed in VSC using the SQLite Viewer found here: https://marketplace.visualstudio.com/items?itemName=qwtel.sqlite-viewer

### 8. User/Admin logins

To login as a admin, you can use the pre-defined login: 

Email: example@example.com
Password: password123

To login as a standard user, you can use the pre-defined login or use the website to register a new login:

Email: Test@Test.com22
Password: Test22

### 9. Testing

Since the IEAP has some areas of improvement, testing may come with some faults. Adhere to the report for understanding on what is the current state of the web application.