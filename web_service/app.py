from flask import Flask, render_template, jsonify, request
import sqlite3

app = Flask(__name__)
DB_FILE = "../historian_data.db"

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

#get historian data to the web "user"
@app.route('/historian', methods=['GET'])
def historian():
    topic = request.args.get('topic',"#")
    timestamp = request.args.get('timestamp',"1970-01-01 00:00:00")

    # todo replace the # by the SQL wildcard (%)
#    topic = topic.replace("#",'\%')

    print(topic)

    SQL = "SELECT timestamp, topic, payload FROM historian_data WHERE timestamp >= ? and topic LIKE ?"

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(SQL,(timestamp,topic))

    results = cursor.fetchall()

    result_data = [{"topic":row[1], "payload":row[2], "timestamp":row[0]} for row in results]

    return jsonify(result_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
