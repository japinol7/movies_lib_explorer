## Movies Library Metadata Explorer

    Movies Library Metadata Explorer using Django.


   * The program 

	program: Movies Library Metadata Explorer using Django.
    name as a package: movies_lib_explorer 
	version: 0.0.1
	author: Joan A. Pinol
	author_nickname: japinol
	author_gitHub: japinol7
	author_twitter: @japinol
	requirements: Django 4.1
	Python requires: 3.10 or greater.
	Python versions tested: 
        > 3.10.10 64bits under Windows 11


## Screenshots

<img src="screenshots/screenshot1.png"> <br/> <br/>
<img src="screenshots/screenshot2.png"> <br/> <br/>
<img src="screenshots/screenshot3.png"> <br/> <br/>
<img src="screenshots/screenshot4.png"> <br/> <br/>
<img src="screenshots/screenshot5.png"> <br/>


**To make this app server work**

	Do this:
	    1. Clone this repository in your local system.
	    2. Go to its folder in your system.
	    3. $ pip install -r requirements.txt
	    4. The first time you must create a new database with the right tables this way:
	       $ python manage.py migrate
	       4.1 You can also create an admin user this way, so you can log in, create other users, etc:
	          $ python manage.py createsuperuser
	    5. $ python manage.py runserver
	    6. Open the website indicated in the console in your browser.
	       Example: http://127.0.0.1:8000/
