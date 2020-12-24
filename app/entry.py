from flask import Flask, request, render_template, jsonify
import logging
import json
from logging.config import dictConfig
import flask_monitoringdashboard as dashboard
from flask_basicauth import BasicAuth
from flasgger import Swagger
from flasgger.utils import swag_from

# logging with log.ini file
logging.basicConfig(level=logging.DEBUG)
with open('log.ini') as f:
    log_set = json.load(f)
    # log_set["handlers"]["api"]["filename"] = "../log/api/api.log"
    dictConfig(log_set)
log = logging.getLogger('api')


def get_user_id():
    return request.environ['REMOTE_ADDR']


# creating app and adding logger in it
app = Flask(__name__)

# flask monitoring dashboard
dashboard.config.init_from(file='config.cfg')
dashboard.config.group_by = get_user_id
dashboard.bind(app)

# flask logging in file
app.logger.addHandler(log)

# swagger for API documentation
# Swagger(app)

# securing endpoints with user names and passwords
app.config['BASIC_AUTH_USERNAME'] = 'username'
app.config['BASIC_AUTH_PASSWORD'] = 'password'
# app.config['BASIC_AUTH_FORCE'] = True # if you want to protect all end points under app
basic_auth = BasicAuth(app)


@app.route('/connect', methods=['GET','POST'])
# @basic_auth.required # this needs to be placed after route line
def connect():
    app.logger.info('Connection Tested OK')
    return 'you are connected!',200


@app.route('/index', methods=['GET','POST'])
# @basic_auth.required # this needs to be placed after route line
def index():
    app.logger.info('Index page requested')
    return render_template("index.html", var1="Liril"),200


@app.route('/double', methods=['POST'])
# @swag_from('endpoint_doc/double.yml')
def double_the_number():
    try:
        result = int(request.form["A"]) + int(request.form["B"])
        return jsonify({"result":result}),200
    except Exception as e:
        app.logger.fatal(e, )
        return 'you asked for error', 500


@app.route('/error', methods=['GET'])
def give_me_error():
    try:
        raise Exception("Error from code")
    except Exception as e:
        app.logger.fatal(e, )
        return 'you asked for error', 500


if __name__ == '__main__':
    app.logger.debug('Application started')
    app.run(host='0.0.0.0', port=3399, debug=True)