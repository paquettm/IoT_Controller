from flask import Flask, render_template, jsonify, request, redirect
import sqlite3
import json

app = Flask(__name__)
DB_FILE = "../historian_data.db"

CONFIG_FILE = "../config.json"
#load the configuration data
with open(CONFIG_FILE, 'r') as config_file:
    config_data = json.load(config_file)

# return a view file
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# return simple text
@app.route('/configure', methods=['GET'])
def configure():
    return render_template('configure.html', config=config_data)

# return JSON from a data source such as a database
@app.route('/add_configuration',methods=['POST'])
def add_configuration():
    topic = request.form.get('topic')
    comparison = request.form.get('comparison')
    value = request.form.get('value')
    result_topic = request.form.get('result_topic')
    result_value = request.form.get('result_value')

    input = {"conditions":[{"topic":topic, "comparison":comparison, "value":value}],"results":[{"topic":result_topic,"value":result_value}]}

    config_data.append(input)

    #rewrite the configuration file
    with open(CONFIG_FILE, 'w') as config_file:
        json.dump(config_data, config_file, indent=4)

    return redirect('/configure')

@app.route('/delete_configuration',methods=['POST'])
def delete_configuration():
    index = int(request.form.get('rule_to_delete'))

    if 0 <= index and index < len(config_data):
        del config_data[index]

        #rewrite the configuration file
        with open(CONFIG_FILE, 'w') as config_file:
            json.dump(config_data, config_file, indent=4)

    return redirect('/configure')

#get historian data to the web "user"
@app.route('/historian', methods=['GET'])
def historian():
    topic = request.args.get('topic',"#")
    timestamp = request.args.get('timestamp',"1970-01-01 00:00:00")

    topic = topic.replace('#','%')

    SQL = "SELECT timestamp, topic, payload FROM historian_data WHERE timestamp >= ? and topic LIKE ?"

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(SQL,(timestamp,topic))

    results = cursor.fetchall()

    result_data = [{"topic":row[1], "payload":row[2], "timestamp":row[0]} for row in results]

    return jsonify(result_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
