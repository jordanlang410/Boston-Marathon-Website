"""
Create a Registration and Login page for the user.
Create a website that allows the user to navigate between 3 routes.
These routes are home.html, boston_marathon_history.html, and boston_marathon_winners.html
"""

from datetime import datetime
import csv
from flask import Flask, render_template, request, url_for, redirect


app = Flask(__name__)

special_char=['$','@','#','*','!','%']

#Read in common passwords file
with open ("CommonPassword.txt", "r") as commonpassfile:
    reader = csv.reader(commonpassfile)
    commonpasswords = list(reader)


@app.route("/", methods = ["GET", "POST"])
def registration():
    """Function to create the registration page for the user to create an account."""

    with open ("save_users.csv", "r") as files:
        # read csv file for usernames and passwords
        read = csv.reader(files)

        usernames = {}
        for row in read:
            usernames[row[0]] = row[1]

    error = ""

    try:

        if request.method == "POST":

            # use form from registration.html and store entries
            attempted_username = request.form.get('name')
            attempted_password = request.form.get('password')

            #validate all entries for username and password. Go to login page once created.
            if not attempted_username or not attempted_password:
                error = "Please enter a username or password."
            elif attempted_username in usernames.keys():
                if usernames.get(attempted_username) == attempted_password:
                    return redirect(url_for('login'))
                else:
                    error = "User already exists"
                    # check user entered password against common passwords txt file
            elif any(i[0] == attempted_password for i in commonpasswords):
                error = "Please pick a less common password."
            elif len(attempted_password) < 12:
                error = "Your password must be more than 12 characters."
            elif not any(char.isdigit() for char in attempted_password):
                error = "Your password must contain a number."
            elif not any(char.isupper() for char in attempted_password):
                error = "Your password must contain a uppercase letter."
            elif not any(char.islower() for char in attempted_password):
                error = "Your password must contain a lowercase letter."
            elif not any(char in special_char for char in attempted_password):
                error = "Your password must contain a special character $,@,#,*,!,%"

            else:
                #Save the username and password once they are validated.
                file = open("save_users.csv", "a", newline='')
                writer = csv.writer(file)
                writer.writerow((attempted_username, attempted_password))
                file.close()

                return redirect(url_for('login'))

        return render_template("registration.html", error = error)

    except Exception as er1:
        return render_template("registration.html", error = error)


@app.route("/login", methods = ["GET", "POST"])
def login():
    """Function to create the login page to allow the user to login."""

    with open ("save_users.csv", "r") as files:
        # read csv file for usernames and passwords
        read = csv.reader(files)

        usernames = {}
        for row in read:
            usernames[row[0]] = row[1]

    error = ""
    try:

        if request.method == "POST":

            #use form from login.html and store entries
            attempted_username = request.form.get('username')
            attempted_password = request.form.get('pass')

            #validate username and password.  Login if they match
            if not attempted_username or not attempted_password:
                error = "Please enter a username or password."
            elif attempted_username in usernames.keys():
                if usernames.get(attempted_username) == attempted_password:
                    return redirect(url_for('home'))
                else:
                    # if username/pass fail, write into failed_logins file to save
                    with open ("failed_logins.csv", "a", newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow((attempted_username, attempted_password, datetime.now()))
                        file.close()
                        error = "Username or Password is incorrect."

            else:
                # if username/pass fail, write into failed_logins file to save
                with open ("failed_logins.csv", "a", newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow((attempted_username, attempted_password, datetime.now()))
                    file.close()
                    error = "Username or Password is incorrect."


        return render_template("login.html", error = error)

    except Exception as er2:
        return render_template("login.html", error = error)


@app.route("/changepass", methods = ["GET", "POST"])
def changepass():
    """
    Function to allow the user to change their password from inside the websites homepage
    if they have a proper username.
    """

    with open ("save_users.csv", "r") as files:
        # read csv file for usernames and passwords
        read = csv.reader(files)

        usernames = {}
        for row in read:
            usernames[row[0]] = row[1]

    error = ""

    try:

        if request.method == "POST":

            #use form from changepass.html and store entries
            attempted_username = request.form.get('userna')
            attempted_password = request.form.get('passwo')

            if not attempted_username or not attempted_password:
                error = "Please enter a username or password."
                # check user entered password against common passwords txt file
            elif any(i[0] == attempted_password for i in commonpasswords):
                error = "Please pick a less common password."
            elif len(attempted_password) < 12:
                error = "Your password must be more than 12 characters."
            elif not any(char.isdigit() for char in attempted_password):
                error = "Your password must contain a number."
            elif not any(char.isupper() for char in attempted_password):
                error = "Your password must contain a uppercase letter."
            elif not any(char.islower() for char in attempted_password):
                error = "Your password must contain a lowercase letter."
            elif not any(char in special_char for char in attempted_password):
                error = "Your password must contain a special character $,@,#,*,!,%"
            elif attempted_username not in usernames.keys():
                error = "User does not exist."

            else:
                usernames[attempted_username] = attempted_password
                file = open("save_users.csv", "w", newline='')
                writer = csv.writer(file)
                # write in only the password the user entered
                for key, value in usernames.items():
                    writer.writerow([key,value])
                file.close()

                return redirect(url_for('login'))

        return render_template("changepass.html", error=error)

    except Exception as er3:
        return render_template("changepass.html", error=error)


@app.route("/home.html")
def home():
    """Function to create the home.html page and display the date/time."""

    return render_template("home.html", datetime = str(datetime.now()))

headings = ("Name", "Nationality", "Time")

data = (
    ("Lawrence Cherono", "Kenya", "2:07:57"),
    ("Lelisa Desisa", "Ethiopia", "2:07:59"),
    ("Kenneth Kipkemoi", "Kenya", "2:08:07"),
    ("Felix Kandie", "Kenya", "2:08:54")
    )


@app.route("/boston_marathon_winners")
def boston_marathon_winners():
    """Function to create the boston_marathon_winners.html page and display the date/time."""
    return render_template("boston_marathon_winners.html",headings=headings,
                           data=data, datetime = str(datetime.now()))


@app.route("/boston_marathon_history")
def boston_marathon_history():
    """Function to create the boston_marathon_.html page and display the date/time."""
    return render_template("boston_marathon_history.html", datetime = str(datetime.now()))


if __name__ == "__main__":
    app.run(debug=True)
