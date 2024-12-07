# simple flask server
from flask import Flask, request, jsonify
import csv
import requests
import os
app = Flask(__name__)

@app.route('/getValue')
def get():
    # extract query params
    date = request.args.get('date')
    from_currency = request.args.get('from')
    to_currency = request.args.get('to')

    value = get_value_from_csv(date=date, from_currency=from_currency, to_currency=to_currency)
    return value



@app.route('/save' , methods=['POST'])
def save():
    request_data = request.get_json()
    url = request_data['url']
    if not url:
            return jsonify({"error": "Missing 'url' in request data"}), 400
    print(url)
    # get the file from the url
    response = requests.get(url)
    # print that csv file
    csv_reader  = csv.reader(response.text.splitlines())
    all_lines = list(row for row in csv_reader)
    print(len(all_lines))
    # Ensure the file exists
    open("data.csv", "a").close()
    merged_set = merge_csv_files(all_lines)
    
            

    with open('data.csv', 'w', newline="") as file:
        csv_writer = csv.writer(file)
        for line in merged_set:
            csv_writer.writerow(line)
    
    return 'Saved!'

def merge_csv_files(another_csv):
    with open("data.csv", "r") as file:
        csv_reader = csv.reader(file)
        all_lines = set(tuple(row) for row in csv_reader)
        another_lines = set(tuple(row) for row in another_csv)
        merged_set = another_lines | all_lines
        print(len(merged_set))
    return merged_set



def get_value_from_csv(date, from_currency , to_currency):
    with open('data.csv', 'r') as file:
        csv_reader = csv.reader(file)
        for line in csv_reader:
            if line[0] == date and line[1] == from_currency and line[2] == to_currency:
                return line[3]
    return 'Value not found!'



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

            