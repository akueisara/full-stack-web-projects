from flask import Flask, request, abort
import hashlib
import datetime

app = Flask(__name__)

login_attempts = 0
lock_time = None


# make a post request
# it should include a json body 
# with a password paramater as a string
@app.route('/login', methods=['POST'])
def headers():
    global login_attempts
    global lock_time
    
    if lock_time is not None:
        if datetime.datetime.now() - lock_time >= datetime.timedelta(hours=1):
            login_attempts = 0
            lock_time = None
        else:
            abort(422)

    if login_attempts >= 5:
        lock_time = datetime.datetime.now()
        abort(422)
    else:
        login_attempts += 1

    data = request.get_json()
    # invalid input format
    if 'password' not in data:
        abort(422)
    elif type(data['password']) is not str:
        abort(422)

    # check password
    # hash the password
    # > this is technically not plain text
    # > you'll learn about hashing soon
    # > we didn't want to make it easy for you to cheat ;)
    digest = hashlib.md5(data['password'].encode()).hexdigest()
    
    # compare the password to the message digest
    if digest == '2f3a4fccca6406e35bcf33e92dd93135':
        return "ACCESS GRANTED"
    else:
        abort(401)