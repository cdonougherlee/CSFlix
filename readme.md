# CSFlix Web Application

## Description


A web application that demonstrates use of Python's Flask framework. The application makes use of libraries such as the Jinja templating library and WTForms. Architectural design patterns and principles including Repository, Dependency Inversion and Single Responsibility have been used to design the application. The application uses Flask Blueprints to maintain a separation of concerns between application functions. Testing includes unit and end-to-end testing using the pytest tool. 


## Somewhere

I didn't make this site responsive so full screen viewing is recommended.


## Steps to install and run the web application

**Assumptions is that Python3 and Git bash are both downloaded and installed on your computer**

Step 1) First open the command prompt, found on Windows by typing cmd in the windows search bar.

Step 2) Navigate to the directory you wish to save the web app's files to. You can navigate directories by typing cd "Directory_name" to move to a desired
directory (e.g. cd Desktop). To go back a directory type cd ..

Step 3) Back in the Assignment-2 repository in GitHub (https://github.com/camdeluxe/Assignment-2), open the green Code tab, then copy the HTTPS link.

Step 4) Now in the command prompt, in the desired directory (e.g. C:\Users\camer\Desktop), clone from the GitHub repository using a Git Bash shell by typing as follows:

```shell 
$ git init
```
Then with the copied HTTPS link:
```shell
$ git clone HTTPS-link
```
e.g. $ git clone https://github.com/camdeluxe/Assignment-2.git

Step 5) Switch to the assignment 2 directory with all the files:
```shell
$ cd Assignment-2
``` 
Step 6) Now to create a virtual environment and install requirements, in the command prompt type the following:
```shell
$ py -3 -m venv venv
$ venv\Scripts\activate
$ pip install -r requirements.txt
```

When using PyCharm, set the virtual environment using 'File'->'Settings' and select 'Project:Assignment-2' from the left menu. Select 'Project Interpreter', click on the gearwheel button and select 'Add'. Click the 'Existing environment' radio button to select the virtual environment. 

## Execution from virtual environment

From the *Assignment-2* directory, and within the activated virtual environment (see *venv\Scripts\activate* above):

**Running the application**

In the command prompt type:

````shell
$ flask run
```` 

You will now see that the web app is running on your computer's local host. This is http://127.0.0.1:5000/ in a browser

--Please note--

If web app seems to be styled incorrectly, it may be that it is the web browser that is caching the stylesheet.
If you're using Chrome, you can disable caching: click F12, network, disable cache.  


## Configuration

The *Assignment-2/.env* file contains variable settings. They are set with appropriate values.

* `FLASK_APP`: Entry point of the application (should always be `wsgi.py`).
* `FLASK_ENV`: The environment in which to run the application (either `development` or `production`).
* `SECRET_KEY`: Secret key used to encrypt session data.
* `TESTING`: Set to False for running the application. Overridden and set to True automatically when testing the application.
* `WTF_CSRF_SECRET_KEY`: Secret key used by the WTForm library.


## Testing from virtual environment

Testing requires that file *Assignment-2/tests/conftest.py* be edited to set the value of `TEST_DATA_PATH`. You should set this to the absolute path of the *Assignment-2/tests/data* directory. 

E.g. 

`TEST_DATA_PATH = os.path.join('C:', os.sep, 'Users', 'camer', 'Desktop', 'Assignment-2', 'tests', 'data')`

assigns TEST_DATA_PATH with the following value (the use of os.path.join and os.sep ensures use of the correct platform path separator):

`C:\Users\camer\Desktop\A place to save stuff\Assignment-2\tests\data`

**Running all tests**

In the command prompt type:

````shell
$ python -m pytest
```` 

You can now also run tests from within PyCharm.

 