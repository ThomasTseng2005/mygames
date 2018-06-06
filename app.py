from flask import Flask, render_template, redirect, url_for, request
from random import randint
from models import User
from models import NumberGuessingGame

app = Flask(__name__)

users = [User("admin", "admin")]
ngg = NumberGuessingGame()
current_user = users[0]
emessage = ""
guesses = {}


@app.route('/')
def hello_world():
    return redirect(url_for('login'))


@app.route('/login', methods=["POST", "GET"])
def login():
    global current_user
    error_message = None
    if request.method == "POST":
        username = request.form["username"]
        for user in users:
            if user.name == username:
                if user.password == request.form["password"]:
                    current_user = user
                    current_user.guessing_number = randint(0, 100)
                    return redirect(url_for('home'))
                else:
                    error_message = "Wrong password!"
            else:
                error_message = "No user by that name!"
        for i in users:
            print(i)

    return render_template("login.html", user=current_user, error_message=error_message)


@app.route('/create', methods=["POST", "GET"])
def create():
    error = None
    if request.method == "POST":
        global current_user
        usersignup = request.form["usersignup"]
        passwordsignup = request.form["passwordsignup"]
        retypesignup = request.form["retype_password"]
        for user in users:
            if user.name == usersignup:
                error = "User signed up already!"
        else:
            if passwordsignup != retypesignup or passwordsignup == "":
                error = "Passwords don't match or password is empty!"
            else:
                current_user = User(usersignup, passwordsignup)
                users.append(current_user)
                return redirect(url_for('home'))
    return render_template("create.html", user=current_user, error_message=error, users=users)


@app.route('/home', methods=["POST", "GET"])
def home():
    global current_user
    global numberguessinggamesame
    numberguessinggamesame = False
    if request.method == "POST":
        option_chosen = request.form["option"]
        print("They chose: ", option_chosen)
        if option_chosen == "Number Guessing Game":
            return redirect(url_for("numberguessinggame"))
        elif option_chosen == "Team Generator":
            return redirect(url_for("tgstart"))
    return render_template("home.html", current_user=current_user, users=users, header=True)


@app.route('/logout')
def logout():
    global current_user
    current_user = None
    return redirect(url_for('login'))


@app.route('/numberguessinggame/new_game')
def numberguessinggame():
    ngg.get_new_number()
    ngg.guesses = {}
    ngg.numberguessinggamesame = False
    return redirect(url_for('numberguessinggame_continue', ngg=ngg))


@app.route('/numberguessinggame/continue_game', methods=["POST", "GET"])
def numberguessinggame_continue():
    if ngg.numberguessinggamesame == True:
        return redirect(url_for('home'))
    global current_user
    global guesses
    message = ""
    if request.method == "POST":
        # add guess to the guess list
        current_guess = request.form["guess"]
        if current_guess.isdigit() == True:
            if int(current_guess) > ngg.number:
                message = "Guess Is Too Big!"
            elif int(current_guess) < ngg.number:
                message = "Guess Is Too Small!"
            else:
                message = "You win!"
                return redirect(url_for("numberguessinggame_finish", message=message))
            ngg.guesses[str(current_guess)] = message
    return render_template("numberguessinggame.html", message= message, ngg=ngg)


@app.route('/numberguessinggame_finish')
def numberguessinggame_finish():
    if ngg.numberguessinggamesame == True:
        return redirect(url_for('home'))
    global current_user
    count = len(ngg.guesses) + 1
    points = 21 - count
    if points > 0:
        current_user.score += points
    ngg.numberguessinggamesame = True
    return render_template("nggfinish.html", count=count, current_user=current_user, ngg=ngg)


@app.route('/tgstart', methods=["POST", "GET"])
def tgstart():
    return render_template("tgstart.html")


@app.route('/profile', methods=["POST", "GET"])
def profile():
    return render_template("profile.html")


if __name__ == '__main__':
    app.run(debug=True)
