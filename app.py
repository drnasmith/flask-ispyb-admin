import random

from flask import Flask, request, render_template
from flask_basicauth import BasicAuth

from admin import admin
import ispyb

app = Flask(__name__)

def generate_password():
    """
    Utility method to generate a password of a given length
    """
    mypassword = ''
    password_length = 8
    characters = 'abcdefhijklmnopqrstuvwxyz0123456789'

    for i in range(password_length):
        index = random.randrange(len(characters))
        mypassword = mypassword + characters[index]

    print("Generated Password for this session: {}".format(mypassword))

    return mypassword

# Using basic authorisation to protect page
app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = generate_password()
app.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(app)

app.secret_key = b'_5asdadf#y2L"F4Q8z\n\xec]/'

# Initialise the application code
ispyb.init_app(app)
admin.init_app(app)

@app.route('/')
def index():
    return render_template('index.html', db_url=app.config['SQLALCHEMY_DATABASE_URI'])

if __name__ == '__main__':
    app.run(debug=True)
