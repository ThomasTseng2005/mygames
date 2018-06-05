from flask import Flask, render_template, redirect, url_for, request
from random import randint
from models import User

app = Flask(__name__)

users = [User("admin", "admin")]
current_user = users[0]
guesses = {}
final_number = 0
numberguessinggamesame = False
emessage = ""


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
            return redirect(url_for("teamgenerator"))
    return render_template("home.html", current_user=current_user, users=users, header=True)


@app.route('/logout')
def logout():
    global current_user
    current_user = None
    return redirect(url_for('login'))


@app.route('/numberguessinggame/new_game')
def numberguessinggame(new_game=""):
    the_number = randint(1, 100) * 1029384756
    return redirect(url_for('numberguessinggame_continue', guesses=guesses, number=the_number))


@app.route('/numberguessinggame/continue_game/<number>', methods=["POST", "GET"])
def numberguessinggame_continue(number):
    if numberguessinggamesame == True:
        return redirect(url_for('home'))
    global current_user
    global guesses
    global final_number
    message = ""
    final_number = int(int(number) / 1029384756)
    print(final_number)
    if request.method == "POST":
        # add guess to the guess list
        current_guess = request.form["guess"]
        if current_guess.isdigit() == True:
            if int(current_guess) > final_number:
                message = "Guess Is Too Big!"
            elif int(current_guess) < final_number:
                message = "Guess Is Too Small!"
            else:
                message = "You win!"
                return redirect(url_for("numberguessinggame_finish", guesses=guesses, number=number, message=message))
            guesses[str(current_guess)] = message
    return render_template("numberguessinggame.html", message=message, guesses=guesses, final_number=final_number)


@app.route('/numberguessinggame_finish')
def numberguessinggame_finish():
    global current_user
    global guesses
    global final_number
    global numberguessinggamesame
    final_number = final_number
    count = len(guesses) + 1
    guesses = {}
    points = 21 - count
    if points > 0:
        current_user.score += points
    numberguessinggamesame = True
    return render_template("nggfinish.html", count=count, guesses=guesses, final_number=final_number, points=points,
                           numberguessinggamesame=numberguessinggamesame, current_user=current_user)


@app.route('/tgstart', methods=["POST", "GET"])
def tgstart():
    return render_template("tgstart.html")


@app.route('/profile', methods=["POST", "GET"])
def profile():
    return render_template("profile.html")


if __name__ == '__main__':
    app.run(debug=True)
