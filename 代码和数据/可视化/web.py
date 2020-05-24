from flask import Flask
from flask import jsonify
from flask import url_for
from flask import render_template
from flask import request
import json


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dynamic/donghu')
def dynamic_donghu():
    return render_template('dynamicMap_donghu.html')

@app.route('/dynamic/guanggu')
def dynamic_guanggu():
    return render_template('dynamicMap_guanggu.html')

@app.route('/static/guanggu')
def static_guanggu():
    return render_template('staticMap_guanggu.html')

@app.route('/honeyHeatMap')
def honeyHeatMap():
    return render_template('honeyHeatMap.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')      # 设置debug=True是为了让代码修改实时生效，而不用每次重启加载