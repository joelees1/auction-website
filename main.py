from auction import app # imports the auction folder as a package

app = app() # runs the web application

if __name__ == "__main__":
    app.run(debug=True) # only runs web server if main.py is ran directly and not just imported