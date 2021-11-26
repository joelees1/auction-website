This piece of software was made to create a flask-based auction website that met the requirements set out in the 5001-assignment brief under project 1. This website would allow users to register for an account, add items to the site that other users could bid for as well as bid on other user’s items that they wanted. Within each feature were several requirements set out to ensure the code written is effective and meets the project brief.

1.	Download the code from the GitHub repository as a zip file, unzip and upload the contents of the master file into a new Codio project, excluding the venv folder.
  a.	It should now look like this:
 

2.	In the terminal type:
  a.	Sudo apt update
  b.	Sudo apt-get install python3-venv
  c.	Python3 -m venv venv
  d.	. venv/bin/activate

3.	Install modules required by typing ‘pip3 install name-of-module’. Modules needed:
  a.	flask
  b.	flask-login
  c.	flask-sqlalchemy

4.	in routes.py, in send_email() amend “josephlees79@gmail.com” in the last line to your email address.

5.	type this in the terminal to run the flask app:
  a.	export FLASK_APP=main
  b.	flask run --host=0.0.0.0

6.	then go to the top of the codio page in Project > Box info > then click the link under “WEB: Static Content”. in the search bar amend the link e.g. https://shrink-poetic.codio-box.uk to https://shrink-poetic-5000.codio-box.uk by adding -5000.

7.	If any problems with the websites contents are occurring, delete database.db from the auction folder and rerun the flask app to start with an empty database.
