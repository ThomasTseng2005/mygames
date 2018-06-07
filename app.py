from flask import Flask, render_template, redirect, url_for, request
from random import randint
from models import User
from models import NumberGuessingGame
from models import TeamGenerator
from models import FourDigits
import random

app = Flask(__name__)

users = [User("admin", "admin")]
ngg = NumberGuessingGame()
tg = TeamGenerator()
current_user = users[0]
emessage = ""
fd = FourDigits()


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
        elif option_chosen == "Four Digits":
            return redirect(url_for("fdstart"))
    return render_template("home.html", current_user=current_user, users=users, header=True)


@app.route('/logout')
def logout():
    global current_user
    current_user = None
    return redirect(url_for('login'))


@app.route('/numberguessinggame/new_game')
def numberguessinggame():
    global current_user
    ngg.get_new_number()
    ngg.guesses = {}
    ngg.numberguessinggamesame = False
    print(ngg.number)
    return redirect(url_for('numberguessinggame_continue', ngg=ngg))


@app.route('/numberguessinggame/continue_game', methods=["POST", "GET"])
def numberguessinggame_continue():
    if ngg.numberguessinggamesame == True:
        return redirect(url_for('home'))
    global current_user
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
    return render_template("numberguessinggame.html", message=message, ngg=ngg)


@app.route('/numberguessinggame_finish')
def numberguessinggame_finish():
    """if ngg.numberguessinggamesame == True:
        return redirect(url_for('home'))
        """
    global current_user
    if ngg.numberguessinggamesame == True:
        return redirect(url_for('home'))
    global current_user
    count = len(ngg.guesses) + 1
    if count < current_user.ngg:
        current_user.ngg = count
    points = 11 - count
    if points > 0:
        current_user.score += points
    ngg.numberguessinggamesame = True
    return render_template("nggfinish.html", count=count, current_user=current_user, ngg=ngg, header=True)


@app.route('/tgstart', methods=["POST", "GET"])
def tgstart():
    if tg.repick == True:
        return redirect(url_for("tgcontinue"))
    tg.reset()
    if request.method == "POST":
        tg.peoplenumber = request.form["people_number"]
        tg.groupnumber = request.form['group_number']
        print(tg.groupnumber)
        print(tg.peoplenumber)
        if tg.peoplenumber.isdigit() == False:
            tg.message = "Please type in positive integers!"
        else:
            if tg.groupnumber.isdigit() == False:
                tg.message = "Please type in positive integers!"
            else:
                tg.groupnumber = int(tg.groupnumber)
                tg.peoplenumber = int(tg.peoplenumber)
                if tg.peoplenumber < 2 or tg.peoplenumber > 10000:
                    tg.message = "Please type in an integer between 2 and 10000!"
                else:
                    if tg.groupnumber > tg.peoplenumber:
                        tg.message = "Please type in an integer for the number of people that is greater than the number of groups!"
                    else:
                        if tg.groupnumber > 1000 or tg.groupnumber < 2:
                            tg.message = "Please type in integers between 2 and 1000!"
                        else:
                            return redirect(url_for('tgcontinue'))
    return render_template("tgstart.html", message=tg.message)


@app.route('/tgcontinue', methods=["POST", "GET"])
def tgcontinue():
    if tg.repick == True:
        count = 1
        random.shuffle(tg.people)
        for person in tg.people:
            tg.everyone[person] = count
            if count == tg.groupnumber:
                count = 1
            else:
                count += 1
        return redirect(url_for("tgfinish"))
    if request.method == "POST":
        people = request.form.getlist("peoplenumber")
        for i in people:
            tg.people.append(i.title())
        for p in tg.people:
            if tg.people.count(p) > 1 or p == "":
                tg.messagetwo = "Please do not leave any text box blank and no duplicates"
            else:
                count = 1
                random.shuffle(tg.people)
                for person in tg.people:
                    tg.everyone[person] = count
                    if count == tg.groupnumber:
                        count = 1
                    else:
                        count += 1
                return redirect(url_for("tgfinish"))
    return render_template("tgcontinue.html", tgpeoplenum=tg.peoplenumber, everyone=tg.everyone, message=tg.messagetwo)


@app.route('/tgfinish', methods=["POST", "GET"])
def tgfinish():
    tg.repick = False
    for p in tg.people:
        if tg.people.index(p) < tg.groupnumber:
            tg.first.append(p)
    if request.method == "POST":
        tg.repick = True
        tg.first = []
        return redirect(url_for("tgstart"))
    return render_template("tgfinish.html", header=True, team_number=tg.groupnumber, teams=tg.everyone,
                           people=tg.people, the_list=tg.first, groupnumber=tg.groupnumber)


@app.route('/fdstart', methods=["POST", "GET"])
def fdstart():
    fd.num = str(randint(1000, 9999))
    for i in fd.num:
        if fd.num.count(i) > 1:
            fd.repeat = True
    while fd.repeat == True:
        fd.num = str(randint(1000, 9999))
        fd.repeat = False
        for i in fd.num:
            if fd.num.count(i) > 1:
                fd.repeat = True
    fd.guesses = {}
    fd.same = False
    print(fd.num)
    return redirect(url_for("fdcontinue"))

@app.route('/fdcontinue', methods=["POST", "GET"])
def fdcontinue():
    if fd.same == True or fd.num == "0000":
        return redirect(url_for('home'))
    fd.a = 0
    fd.b = 0
    message = ""
    if request.method == "POST":
        print(fd.num)
        current_guess = str(request.form["guess"])
        fd.repeattwo = False
        if current_guess.isdigit() == True:
            for char in current_guess:
                if current_guess.count(char) > 1:
                    fd.repeattwo = True
            if fd.repeattwo == True or len(current_guess) != 4:
                message = "You could only type in four unique digits!"
            else:
                for char in current_guess:
                    if char in fd.num:
                        if current_guess.index(char) == fd.num.index(char):
                            fd.a += 1
                        else:
                            fd.b += 1
                message = str(fd.a) + "a and " + str(fd.b) + "b!"
                fd.guesses[str(current_guess)] = message
                if fd.a == 4:
                    return redirect(url_for("fdfinish", message=message, guesses=fd.guesses, number= fd.num))
    return render_template("fdcontinue.html", message=message, guesses=fd.guesses, number= fd.num)


@app.route('/fdfinish', methods=["POST", "GET"])
def fdfinish():
    global current_user
    if fd.same == True:
        return redirect(url_for('home'))
    count = len(fd.guesses)
    if count < current_user.fd:
        current_user.fd = count
    points = 21 - count
    if points > 0:
        current_user.score += points
    fd.same = True
    return render_template("fdfinish.html", count=count, current_user=current_user, header=True, number= fd.num)


@app.route('/profile', methods=["POST", "GET"])
def profile():
    return render_template("profile.html")


@app.route('/scoreboard', methods=["POST", "GET"])
def scoreboard():
    global users
    global current_user
    return render_template("scoreboard.html", users=users, header=True, current_user=current_user)


if __name__ == '__main__':
    app.run(debug=True)
