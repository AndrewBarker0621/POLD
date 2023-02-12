import json
import time

from flask import Flask, request, jsonify
from flask import render_template

from flask_script import Manager
from livereload import Server

from mysql import Mysql

app = Flask(__name__)
manager = Manager(app)


@app.route('/lidar/', methods=['GET'])
def name():
    db = Mysql()
    plans = db.getPlan()

    return render_template('lidar.html', plans=plans)


@manager.command
def dev():
    live_server = Server(app.wsgi_app)
    live_server.watch('**/*.*')
    live_server.serve(open_url=True)


@app.route("/data")
def data():
    # define some data
    with open('./templates/data.json', 'r') as my_file:
        js_data = my_file.read()
    return js_data  # convert your data to JSON and return


if __name__ == '__main__':
    app.run(app.run(debug=True, port=2008, host='0.0.0.0'))
    manager.run()

# http://3.25.60.79:2008/lidar
