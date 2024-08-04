import os
from services.db.db_handler import create_db, insert_data
from flask import Flask, request, jsonify
from openai import OpenAI
API_KEY = os.getenv("API_KEY")

print(f"API_KEY: {API_KEY}")
app = Flask(__name__)
id=1

hostname = os.getenv('DB_HOST')
database = os.getenv('DB_NAME')
username = os.getenv('DB_USER')
pwd = os.getenv('DB_PASS')
port_id = os.getenv('DB_PORT')
table_name ="data"
    #os.getenv('TABLE_NAME'))



import psycopg2

DB_CONNECTION = None


def create_db_conn():
    global DB_CONNECTION
    if DB_CONNECTION is None:
        DB_CONNECTION = psycopg2.connect(password=pwd, database=database, user=username, host=hostname)
    return DB_CONNECTION
conn = create_db_conn()
create_db(table_name, conn)

@app.route('/ask', methods=['POST'])
def ask():
    global id
    data = request.get_json()
    question = data.get('question')
    if not question:
        return jsonify({'error'}), 400
    try:
        client = OpenAI(api_key=API_KEY)
        completion = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[{"role": "user", "content": question}])
        print(question)
        response = completion.choices[0].message.content
        print(response)
        insert_data(id, question, response,table_name, conn)
        id+=1
        print(id)
        print(f"Finished {id}")
        return jsonify({'question':question},{'answer': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
