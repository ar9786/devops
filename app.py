from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import json

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def get_data():
    try:
        with open('data.json', 'r') as file:
            data = json.load(file)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

# Replace with your actual MongoDB Atlas URI
MONGO_URI = "mongodb+srv://ar9786:tlkKPx2MCYTHwR2m@cluster.uhreqi9.mongodb.net/"
client = MongoClient(MONGO_URI)
db = client["myDatabase"]
collection = db["myCollection"]

@app.route('/form', methods=['GET', 'POST'])
def form():
    error_message = None
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')

        if not name or not email:
            error_message = "Name and Email are required."
        else:
            try:
                collection.insert_one({'name': name, 'email': email})
                return redirect(url_for('success'))
            except PyMongoError as e:
                error_message = f"Database Error: {str(e)}"

    return render_template('form.html', error=error_message)

@app.route('/success')
def success():
    return render_template('success.html')


@app.route('/submittodoitem', methods=['GET','POST'])
def submit_todo_item():
    error_message = None
    if request.method == 'POST':
        item_name = request.form.get('itemName')
        item_description = request.form.get('itemDescription')

        if not item_name or not item_description:
            error_message = "Both fields are required."
        else:
            try:
                collection.insert_one({
                    'itemName': item_name,
                    'itemDescription': item_description
                })
                return redirect(url_for('success'))
            except PyMongoError as e:
                error_message = f"Database Error: {str(e)}"

    return render_template('todo.html', error=error_message)



if __name__ == '__main__':
    app.run(debug=True)
