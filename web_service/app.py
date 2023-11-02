from flask import Flask, render_template, jsonify

app = Flask(__name__)

# return a view file
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# return simple text
@app.route('/example', methods=['GET'])
def example():
    return 'example'

# return JSON from a data source such as a database
@app.route('/service',methods=['GET'])
def service():
    data = [1,2,3,4]
    return jsonify(data)

if __name__ == '__main__':
    app.run() #this will only accept requests from localhost...
