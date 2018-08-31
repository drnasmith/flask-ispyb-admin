from flask import Flask, request, render_template
from flask_basicauth import BasicAuth

from admin import admin
import ispyb

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = 'integration'
app.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(app)

app.secret_key = b'_5asdadf#y2L"F4Q8z\n\xec]/'

ispyb.init_app(app)
admin.init_app(app)

@app.route('/ispyb')
def index():
    return render_template('test.html')

if __name__ == '__main__':
    app.run(debug=True, port=9000)
